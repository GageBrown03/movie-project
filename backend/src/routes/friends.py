# backend/src/routes/friends.py
# Friend system API routes for Flask - WITH ERROR HANDLING

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, User, Friendship, FriendshipStatus
from src.routes.activity_routes import create_activity
from datetime import datetime

friends = Blueprint('friends', __name__, url_prefix='/api/friends')


# ==========================================
# Explicit OPTIONS handler (prevent caching)
# ==========================================
@friends.route('/', methods=['OPTIONS'])
@friends.route('/pending', methods=['OPTIONS'])
@friends.route('/search', methods=['OPTIONS'])
@friends.route('/request', methods=['OPTIONS'])
@friends.route('/accept/<int:friendship_id>', methods=['OPTIONS'])
@friends.route('/decline/<int:friendship_id>', methods=['OPTIONS'])
@friends.route('/<int:friendship_id>', methods=['OPTIONS'])
def handle_options(friendship_id=None):
    """Handle CORS preflight for all friend routes"""
    return '', 204


# ==========================================
# Helper Functions
# ==========================================

def normalize_user_ids(user_id_1, user_id_2):
    """Ensure user_id_1 < user_id_2 for normalized storage"""
    # CRITICAL: Convert to int (get_jwt_identity returns string!)
    id1 = int(user_id_1)
    id2 = int(user_id_2)
    
    if id1 < id2:
        return id1, id2
    return id2, id1


def get_friendship(user_id_1, user_id_2):
    """Get friendship between two users (if exists)"""
    normalized_id_1, normalized_id_2 = normalize_user_ids(user_id_1, user_id_2)
    
    return Friendship.query.filter_by(
        user_id_1=normalized_id_1,
        user_id_2=normalized_id_2
    ).first()


def are_friends(user_id_1, user_id_2):
    """Check if two users are friends"""
    friendship = get_friendship(user_id_1, user_id_2)
    return friendship and friendship.status == FriendshipStatus.ACCEPTED


# ==========================================
# GET /api/friends - Get all friends
# ==========================================

@friends.route('/', methods=['GET'])
@jwt_required()
def get_friends():
    """Get all accepted friends for current user"""
    try:
        current_user_id = int(get_jwt_identity())  # Convert to int
        
        # Query friendships where user is either user_id_1 or user_id_2
        friendships = Friendship.query.filter(
            db.or_(
                Friendship.user_id_1 == current_user_id,
                Friendship.user_id_2 == current_user_id
            ),
            Friendship.status == FriendshipStatus.ACCEPTED
        ).all()
        
        # Build response
        friends_list = []
        for friendship in friendships:
            friend_id = (friendship.user_id_2 
                        if friendship.user_id_1 == current_user_id 
                        else friendship.user_id_1)
            
            friend = User.query.get(friend_id)
            if friend:
                friends_list.append({
                    'friendshipId': friendship.friendship_id,
                    'friendUserId': friend.user_id,
                    'friendUsername': friend.username,
                    'friendDisplayName': friend.display_name,
                    'friendEmail': friend.email,
                    'createdAt': friendship.created_at.isoformat() if friendship.created_at else None,
                    'acceptedAt': friendship.accepted_at.isoformat() if friendship.accepted_at else None,
                })
        
        return jsonify(friends_list), 200
    except Exception as e:
        print(f"Error in get_friends: {str(e)}")
        return jsonify({'error': 'Failed to load friends', 'message': str(e)}), 500


# ==========================================
# GET /api/friends/pending - Get pending requests
# ==========================================

@friends.route('/pending', methods=['GET'])
@jwt_required()
def get_pending_requests():
    """Get all pending friend requests (sent and received)"""
    try:
        current_user_id = int(get_jwt_identity())  # Convert to int
        
        friendships = Friendship.query.filter(
            db.or_(
                Friendship.user_id_1 == current_user_id,
                Friendship.user_id_2 == current_user_id
            ),
            Friendship.status == FriendshipStatus.PENDING
        ).all()
        
        requests_list = []
        for friendship in friendships:
            request_type = 'sent' if friendship.requested_by == current_user_id else 'received'
            
            other_user_id = (friendship.user_id_2 
                            if friendship.user_id_1 == current_user_id 
                            else friendship.user_id_1)
            other_user = User.query.get(other_user_id)
            
            if other_user:
                requests_list.append({
                    'friendshipId': friendship.friendship_id,
                    'requestType': request_type,
                    'requestedBy': friendship.requested_by,
                    'otherUserId': other_user.user_id,
                    'otherUsername': other_user.username,
                    'otherDisplayName': other_user.display_name,
                    'createdAt': friendship.created_at.isoformat() if friendship.created_at else None,
                })
        
        return jsonify(requests_list), 200
    except Exception as e:
        print(f"Error in get_pending_requests: {str(e)}")
        return jsonify({'error': 'Failed to load pending requests', 'message': str(e)}), 500


# ==========================================
# POST /api/friends/request - Send friend request
# ==========================================

@friends.route('/request', methods=['POST'])
@jwt_required()
def send_friend_request():
    """Send a friend request to another user"""
    try:
        current_user_id = int(get_jwt_identity())  # Convert to int
        data = request.get_json()
        
        username = data.get('username')
        email = data.get('email')
        
        if not username and not email:
            return jsonify({'error': 'Username or email required'}), 400
        
        # Find target user
        if username:
            target_user = User.query.filter_by(username=username).first()
        else:
            target_user = User.query.filter_by(email=email).first()
        
        if not target_user:
            return jsonify({'error': 'User not found'}), 404
        
        target_user_id = target_user.user_id
        
        # Prevent self-friending
        if current_user_id == target_user_id:
            return jsonify({'error': 'Cannot send friend request to yourself'}), 400
        
        # Check if friendship already exists
        existing = get_friendship(current_user_id, target_user_id)
        
        if existing:
            if existing.status == FriendshipStatus.ACCEPTED:
                return jsonify({'error': 'Already friends'}), 400
            elif existing.status == FriendshipStatus.PENDING:
                return jsonify({'error': 'Friend request already pending'}), 400
            elif existing.status == FriendshipStatus.DECLINED:
                existing.status = FriendshipStatus.PENDING
                existing.requested_by = current_user_id
                existing.created_at = datetime.utcnow()
                db.session.commit()
                return jsonify({'message': 'Friend request re-sent', 'friendshipId': existing.friendship_id}), 200
        
        # Create new friend request
        normalized_id_1, normalized_id_2 = normalize_user_ids(current_user_id, target_user_id)
        
        friendship = Friendship(
            user_id_1=normalized_id_1,
            user_id_2=normalized_id_2,
            requested_by=current_user_id
        )
        
        db.session.add(friendship)
        db.session.commit()
        
        return jsonify({
            'message': 'Friend request sent',
            'friendshipId': friendship.friendship_id,
            'targetUsername': target_user.username
        }), 201
    except Exception as e:
        print(f"Error in send_friend_request: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to send friend request', 'message': str(e)}), 500


# ==========================================
# POST /api/friends/accept/<friendship_id>
# ==========================================

@friends.route('/accept/<int:friendship_id>', methods=['POST'])
@jwt_required()
def accept_friend_request(friendship_id):
    """Accept a friend request"""
    try:
        current_user_id = int(get_jwt_identity())  # Convert to int
        
        friendship = Friendship.query.get(friendship_id)
        
        if not friendship:
            return jsonify({'error': 'Friend request not found'}), 404
        
        if friendship.requested_by == current_user_id:
            return jsonify({'error': 'Cannot accept your own friend request'}), 403
        
        if friendship.user_id_1 != current_user_id and friendship.user_id_2 != current_user_id:
            return jsonify({'error': 'Not authorized'}), 403
        
        if friendship.status != FriendshipStatus.PENDING:
            return jsonify({'error': 'Request is not pending'}), 400
        
        friendship.status = FriendshipStatus.ACCEPTED
        friendship.accepted_at = datetime.utcnow()
        db.session.commit()
        
        # ACTIVITY TRACKING: Create activities for both users
        # Activity for current user (accepter)
        create_activity(
            user_id=current_user_id,
            activity_type='friend_added',
            friend_user_id=friendship.user_id_1 if friendship.user_id_2 == current_user_id else friendship.user_id_2
        )
        
        # Activity for requester
        other_user_id = friendship.user_id_1 if friendship.user_id_2 == current_user_id else friendship.user_id_2
        create_activity(
            user_id=other_user_id,
            activity_type='friend_added',
            friend_user_id=current_user_id
        )
        
        return jsonify({'message': 'Friend request accepted'}), 200
    except Exception as e:
        print(f"Error in accept_friend_request: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to accept request', 'message': str(e)}), 500


# ==========================================
# POST /api/friends/decline/<friendship_id>
# ==========================================

@friends.route('/decline/<int:friendship_id>', methods=['POST'])
@jwt_required()
def decline_friend_request(friendship_id):
    """Decline a friend request"""
    try:
        current_user_id = int(get_jwt_identity())  # Convert to int
        
        friendship = Friendship.query.get(friendship_id)
        
        if not friendship:
            return jsonify({'error': 'Friend request not found'}), 404
        
        if friendship.requested_by == current_user_id:
            return jsonify({'error': 'Cannot decline your own friend request'}), 403
        
        if friendship.user_id_1 != current_user_id and friendship.user_id_2 != current_user_id:
            return jsonify({'error': 'Not authorized'}), 403
        
        if friendship.status != FriendshipStatus.PENDING:
            return jsonify({'error': 'Request is not pending'}), 400
        
        friendship.status = FriendshipStatus.DECLINED
        db.session.commit()
        
        return jsonify({'message': 'Friend request declined'}), 200
    except Exception as e:
        print(f"Error in decline_friend_request: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to decline request', 'message': str(e)}), 500


# ==========================================
# DELETE /api/friends/<friendship_id>
# ==========================================

@friends.route('/<int:friendship_id>', methods=['DELETE'])
@jwt_required()
def remove_friend(friendship_id):
    """Remove a friend or cancel friend request"""
    try:
        current_user_id = int(get_jwt_identity())  # Convert to int
        
        friendship = Friendship.query.get(friendship_id)
        
        if not friendship:
            return jsonify({'error': 'Friendship not found'}), 404
        
        if friendship.user_id_1 != current_user_id and friendship.user_id_2 != current_user_id:
            return jsonify({'error': 'Not authorized'}), 403
        
        db.session.delete(friendship)
        db.session.commit()
        
        return jsonify({'message': 'Friend removed'}), 200
    except Exception as e:
        print(f"Error in remove_friend: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to remove friend', 'message': str(e)}), 500


# ==========================================
# GET /api/friends/search?q=username
# ==========================================

@friends.route('/search', methods=['GET'])
@jwt_required()
def search_users():
    """Search for users by username"""
    try:
        current_user_id = int(get_jwt_identity())  # Convert to int
        query = request.args.get('q', '')
        
        print(f"Search query: '{query}' from user {current_user_id}")
        
        if len(query) < 2:
            return jsonify({'error': 'Search query must be at least 2 characters'}), 400
        
        # Search for users (only searchable profiles)
        # Use .is_(True) instead of == True for proper SQLAlchemy boolean comparison
        users = User.query.filter(
            User.username.ilike(f'%{query}%'),
            User.user_id != current_user_id,
            User.privacy_profile_searchable.is_(True)
        ).limit(20).all()
        
        print(f"Found {len(users)} searchable users")
        
        # Check friendship status for each user
        results = []
        for user in users:
            friendship = get_friendship(current_user_id, user.user_id)
            
            results.append({
                'userId': user.user_id,
                'username': user.username,
                'displayName': user.display_name,
                'friendshipStatus': friendship.status.value if friendship else None,
                'friendshipId': friendship.friendship_id if friendship else None,
            })
        
        print(f"Returning {len(results)} results")
        return jsonify(results), 200
        
    except Exception as e:
        print(f"Error in search_users: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Search failed', 'message': str(e)}), 500