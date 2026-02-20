# backend/src/routes/activity_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, Activity, User, Friendship, Media, MediaStatus, FriendshipStatus
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, desc

activity_bp = Blueprint('activity', __name__, url_prefix='/api/activity')


def create_activity(user_id, activity_type, media_id=None, friend_user_id=None, data=None):
    """
    Helper function to create an activity.
    Call this from other routes when actions happen.
    
    Args:
        user_id: ID of user performing action
        activity_type: 'rating', 'watchlist', 'friend_added'
        media_id: ID of related media (optional)
        friend_user_id: ID of friend (optional)
        data: Dict with extra data (rating value, etc.)
    """
    try:
        activity = Activity(
            user_id=user_id,
            activity_type=activity_type,
            media_id=media_id,
            friend_user_id=friend_user_id,
            data=data or {}
        )
        db.session.add(activity)
        db.session.commit()
        return activity
    except Exception as e:
        db.session.rollback()
        print(f"Error creating activity: {e}")
        return None


@activity_bp.route('/feed', methods=['GET'])
@jwt_required()
def get_activity_feed():
    """
    Get activity feed (user's own activities + friends' activities)
    Query params:
        - limit: Number of items (default 50)
        - offset: Pagination offset (default 0)
        - filter: 'all', 'me', 'friends' (default 'all')
    """
    try:
        current_user_id = int(get_jwt_identity())
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        filter_type = request.args.get('filter', 'all')
        
        # Get user's friends (using normalized friendship table)
        friend_ids = []
        try:
            # Get friendships where current user is user_id_1
            friends_1 = db.session.query(Friendship.user_id_2).filter(
                Friendship.user_id_1 == current_user_id,
                Friendship.status == FriendshipStatus.ACCEPTED
            ).all()
            
            # Get friendships where current user is user_id_2
            friends_2 = db.session.query(Friendship.user_id_1).filter(
                Friendship.user_id_2 == current_user_id,
                Friendship.status == FriendshipStatus.ACCEPTED
            ).all()
            
            # Combine and extract IDs
            friend_ids = [f[0] for f in friends_1] + [f[0] for f in friends_2]
        except Exception as e:
            print(f"Error loading friends: {e}")
            # Continue with empty friend list
        
        # Build query based on filter
        query = Activity.query
        
        if filter_type == 'me':
            query = query.filter(Activity.user_id == current_user_id)
        elif filter_type == 'friends':
            if not friend_ids:
                return jsonify([]), 200
            query = query.filter(Activity.user_id.in_(friend_ids))
        else:  # 'all'
            user_ids = [current_user_id] + friend_ids
            query = query.filter(Activity.user_id.in_(user_ids))
        
        # Get activities with eager loading
        activities = query.order_by(desc(Activity.created_at)).limit(limit).offset(offset).all()
        
        # Convert to dict with error handling, and filter out activities with deleted media
        result = []
        for activity in activities:
            try:
                activity_dict = activity.to_dict()
                
                # Skip activities for rating/watchlist if media was deleted
                if activity.activity_type in ['rating', 'watchlist']:
                    if not activity.media or not activity.media_id:
                        continue  # Skip this activity
                
                result.append(activity_dict)
            except Exception as e:
                print(f"Error converting activity {activity.activity_id} to dict: {e}")
                # Skip this activity if it causes errors
                continue
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error fetching activity feed: {e}")
        return jsonify({'error': 'Failed to fetch activity feed'}), 500


@activity_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_activity(user_id):
    """
    Get activity feed for a specific user.
    Used for user profile pages.
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        
        activities = Activity.query.filter_by(user_id=user_id).order_by(
            desc(Activity.created_at)
        ).limit(limit).all()
        
        # Convert to dict with error handling, filter out deleted media
        result = []
        for activity in activities:
            try:
                activity_dict = activity.to_dict()
                
                # Skip activities for rating/watchlist if media was deleted
                if activity.activity_type in ['rating', 'watchlist']:
                    if not activity.media or not activity.media_id:
                        continue  # Skip this activity
                
                result.append(activity_dict)
            except Exception as e:
                print(f"Error converting activity {activity.activity_id} to dict: {e}")
                continue
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error fetching user activity: {e}")
        return jsonify({'error': 'Failed to fetch user activity'}), 500

@activity_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_activity_stats():
    """
    Get current activity stats for the Hero section.
    Queries direct tables for accurate, real-time totals.
    """
    try:
        current_user_id = int(get_jwt_identity())
        
        # 1. Total Rated: Count items in Media table where this user has a rating
        total_rated = Media.query.filter(
            Media.user_id == current_user_id,
            Media.rating != None
        ).count()
        
        # 2. Total Watchlist: Count items with 'want_to_watch' status
        total_watchlist = Media.query.filter(
            Media.user_id == current_user_id,
            Media.status == MediaStatus.WANT_TO_WATCH
        ).count()
        
        # 3. Total Friends: Count accepted friendships where user is participant 1 or 2
        total_friends = Friendship.query.filter(
            or_(
                Friendship.user_id_1 == current_user_id, 
                Friendship.user_id_2 == current_user_id
            ),
            Friendship.status == FriendshipStatus.ACCEPTED
        ).count()
        
        # Return the keys exactly as HomeView.vue expects them
        return jsonify({
            'totalRated': total_rated,
            'totalWatchlist': total_watchlist,
            'totalFriends': total_friends
        }), 200
        
    except Exception as e:
        print(f"Error fetching activity stats: {e}")
        return jsonify({'error': 'Failed to fetch activity stats'}), 500