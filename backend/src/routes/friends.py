# backend/src/routes/friends.py
# Friend system API routes for Flask

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, User, Friendship, FriendshipStatus
from datetime import datetime

friends = Blueprint('friends', __name__, url_prefix='/api/friends')


# ==========================================
# Helper Functions
# ==========================================

def normalize_user_ids(user_id_1, user_id_2):
    """Ensure user_id_1 < user_id_2 for normalized storage"""
    if user_id_1 < user_id_2:
        return user_id_1, user_id_2
    return user_id_2, user_id_1


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
    current_user_id = get_jwt_identity()
    
    # Query friendships where user is either user_id_1 or user_id_2
    # and status is accepted
    friendships = Friendship.query.filter(
        db.or_(
            Friendship.user_id_1 == current_user_id,
            Friendship.user_id_2 == current_user_id
        ),
        Friendship.status == FriendshipStatus.ACCEPTED
    ).all()
    
    # Build response with friend details
    friends_list = []
    for friendship in friendships:
        # Determine which user is the friend
        friend_id = (friendship.user_id_2 
                    if friendship.user_id_1 == current_user_id 
                    else friendship.user_id_1)
        
        # Get friend's info
        friend = User.query.get(friend_id)
        
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


# ==========================================
# GET /api/friends/pending - Get pending requests
# ==========================================

@friends.route('/pending', methods=['GET'])
@jwt_required()
def get_pending_requests():
    """Get all pending friend requests (sent and received)"""
    current_user_id = get_jwt_identity()
    
    # Query all pending friendships involving this user
    friendships = Friendship.query.filter(
        db.or_(
            Friendship.user_id_1 == current_user_id,
            Friendship.user_id_2 == current_user_id
        ),
        Friendship.status == FriendshipStatus.PENDING
    ).all()
    
    # Build response
    requests_list = []
    for friendship in friendships:
        # Determine if sent or received
        request_type = 'sent' if friendship.requested_by == current_user_id else 'received'
        
        # Get other user's info
        other_user_id = (friendship.user_id_2 
                        if friendship.user_id_1 == current_user_id 
                        else friendship.user_id_1)
        other_user = User.query.get(other_user_id)
        
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


# ==========================================
# POST /api/friends/request - Send friend request
# ==========================================

@friends.route('/request', methods=['POST'])
@jwt_required()
def send_friend_request():
    """Send a friend request to another user"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get target user by username or email
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
            # Allow re-requesting after decline
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
    
    # TODO: Send email notification (if email service configured)
    
    return jsonify({
        'message': 'Friend request sent',
        'friendshipId': friendship.friendship_id,
        'targetUsername': target_user.username
    }), 201


# ==========================================
# POST /api/friends/accept/<friendship_id>
# ==========================================

@friends.route('/accept/<int:friendship_id>', methods=['POST'])
@jwt_required()
def accept_friend_request(friendship_id):
    """Accept a friend request"""
    current_user_id = get_jwt_identity()
    
    # Get friendship
    friendship = Friendship.query.get(friendship_id)
    
    if not friendship:
        return jsonify({'error': 'Friend request not found'}), 404
    
    # Verify user is recipient (not requester)
    if friendship.requested_by == current_user_id:
        return jsonify({'error': 'Cannot accept your own friend request'}), 403
    
    # Verify user is part of the friendship
    if friendship.user_id_1 != current_user_id and friendship.user_id_2 != current_user_id:
        return jsonify({'error': 'Not authorized'}), 403
    
    # Verify status is pending
    if friendship.status != FriendshipStatus.PENDING:
        return jsonify({'error': 'Request is not pending'}), 400
    
    # Accept friendship
    friendship.status = FriendshipStatus.ACCEPTED
    friendship.accepted_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Friend request accepted'}), 200


# ==========================================
# POST /api/friends/decline/<friendship_id>
# ==========================================

@friends.route('/decline/<int:friendship_id>', methods=['POST'])
@jwt_required()
def decline_friend_request(friendship_id):
    """Decline a friend request"""
    current_user_id = get_jwt_identity()
    
    # Get friendship
    friendship = Friendship.query.get(friendship_id)
    
    if not friendship:
        return jsonify({'error': 'Friend request not found'}), 404
    
    # Verify user is recipient
    if friendship.requested_by == current_user_id:
        return jsonify({'error': 'Cannot decline your own friend request'}), 403
    
    # Verify user is part of the friendship
    if friendship.user_id_1 != current_user_id and friendship.user_id_2 != current_user_id:
        return jsonify({'error': 'Not authorized'}), 403
    
    # Verify status is pending
    if friendship.status != FriendshipStatus.PENDING:
        return jsonify({'error': 'Request is not pending'}), 400
    
    # Decline friendship
    friendship.status = FriendshipStatus.DECLINED
    db.session.commit()
    
    return jsonify({'message': 'Friend request declined'}), 200


# ==========================================
# DELETE /api/friends/<friendship_id>
# ==========================================

@friends.route('/<int:friendship_id>', methods=['DELETE'])
@jwt_required()
def remove_friend(friendship_id):
    """Remove a friend or cancel friend request"""
    current_user_id = get_jwt_identity()
    
    # Get friendship
    friendship = Friendship.query.get(friendship_id)
    
    if not friendship:
        return jsonify({'error': 'Friendship not found'}), 404
    
    # Verify user is part of the friendship
    if friendship.user_id_1 != current_user_id and friendship.user_id_2 != current_user_id:
        return jsonify({'error': 'Not authorized'}), 403
    
    # Delete friendship
    db.session.delete(friendship)
    db.session.commit()
    
    return jsonify({'message': 'Friend removed'}), 200


# ==========================================
# GET /api/friends/search?q=username
# ==========================================

@friends.route('/search', methods=['GET'])
@jwt_required()
def search_users():
    """Search for users by username"""
    current_user_id = get_jwt_identity()
    query = request.args.get('q', '')
    
    if len(query) < 2:
        return jsonify({'error': 'Search query must be at least 2 characters'}), 400
    
    # Search for users (only searchable profiles)
    users = User.query.filter(
        User.username.ilike(f'%{query}%'),
        User.user_id != current_user_id,
        User.privacy_profile_searchable == True
    ).limit(20).all()
    
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
    
    return jsonify(results), 200