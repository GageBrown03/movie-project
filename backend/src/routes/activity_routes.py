# backend/src/routes/activity_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, Activity, User, Friendship, Media, MediaStatus
from sqlalchemy import or_, and_, desc

activity_bp = Blueprint('activity', __name__, url_prefix='/api/activity')


def create_activity(user_id, activity_type, media_id=None, friend_user_id=None, data=None):
    """
    Helper function to create an activity.
    Call this from other routes when actions happen.
    
    Args:
        user_id: ID of user performing action
        activity_type: 'rating', 'watchlist', 'friend_added', 'milestone'
        media_id: ID of related media (optional)
        friend_user_id: ID of friend (optional)
        data: Dict with extra data (rating value, milestone type, etc.)
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


def check_milestones(user_id):
    """
    Check if user hit any milestones and create activity if so.
    Call this after adding media.
    """
    # Count total rated items
    total_rated = Media.query.filter_by(
        user_id=user_id, 
        status=MediaStatus.WATCHED
    ).count()
    
    # Milestone thresholds
    milestones = [1, 5, 10, 25, 50, 100, 250, 500]
    
    if total_rated in milestones:
        create_activity(
            user_id=user_id,
            activity_type='milestone',
            data={
                'milestone_type': 'total_rated',
                'count': total_rated
            }
        )


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
    current_user_id = int(get_jwt_identity())
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    filter_type = request.args.get('filter', 'all')
    
    # Get user's friends (using normalized friendship table)
    from src.models import FriendshipStatus
    
    friend_ids_query = db.session.query(Friendship.user_id_1).filter(
        Friendship.user_id_2 == current_user_id,
        Friendship.status == FriendshipStatus.ACCEPTED
    ).union(
        db.session.query(Friendship.user_id_2).filter(
            Friendship.user_id_1 == current_user_id,
            Friendship.status == FriendshipStatus.ACCEPTED
        )
    )
    friend_ids = [f[0] for f in friend_ids_query.all()]
    
    # Build query based on filter
    query = Activity.query
    
    if filter_type == 'me':
        query = query.filter(Activity.user_id == current_user_id)
    elif filter_type == 'friends':
        if friend_ids:
            query = query.filter(Activity.user_id.in_(friend_ids))
        else:
            return jsonify([]), 200  # No friends
    else:  # 'all'
        if friend_ids:
            query = query.filter(
                or_(
                    Activity.user_id == current_user_id,
                    Activity.user_id.in_(friend_ids)
                )
            )
        else:
            query = query.filter(Activity.user_id == current_user_id)
    
    # Get activities
    activities = query.order_by(desc(Activity.created_at)).limit(limit).offset(offset).all()
    
    return jsonify([activity.to_dict() for activity in activities]), 200


@activity_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_activity(user_id):
    """
    Get activity feed for a specific user
    Query params:
        - limit: Number of items (default 50)
    """
    current_user_id = int(get_jwt_identity())
    limit = request.args.get('limit', 50, type=int)
    
    # TODO: Add privacy check when privacy module is ready
    # from src.routes.privacy import can_view_profile
    # if not can_view_profile(current_user_id, user_id):
    #     return jsonify({'error': 'Cannot view this user\'s activity'}), 403
    
    activities = Activity.query.filter_by(user_id=user_id).order_by(
        desc(Activity.created_at)
    ).limit(limit).all()
    
    return jsonify([activity.to_dict() for activity in activities]), 200


@activity_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_activity_stats():
    """Get activity statistics for current user"""
    current_user_id = int(get_jwt_identity())
    from src.models import FriendshipStatus
    
    # Calculate stats
    total_rated = Media.query.filter_by(
        user_id=current_user_id, 
        status=MediaStatus.WATCHED
    ).count()
    
    total_watchlist = Media.query.filter_by(
        user_id=current_user_id, 
        status=MediaStatus.WANT_TO_WATCH
    ).count()
    
    # Count friends (normalized table - user can be in either position)
    total_friends = Friendship.query.filter(
        or_(
            Friendship.user_id_1 == current_user_id,
            Friendship.user_id_2 == current_user_id
        ),
        Friendship.status == FriendshipStatus.ACCEPTED
    ).count()
    
    # Recent activity count (last 7 days)
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_activity_count = Activity.query.filter(
        Activity.user_id == current_user_id,
        Activity.created_at >= week_ago
    ).count()
    
    return jsonify({
        'totalRated': total_rated,
        'totalWatchlist': total_watchlist,
        'totalFriends': total_friends,
        'recentActivityCount': recent_activity_count
    }), 200