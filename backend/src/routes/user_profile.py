# backend/src/routes/user_profile.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, User, Media, Friendship, FriendshipStatus
from sqlalchemy import or_, and_

user_profile_bp = Blueprint('user_profile', __name__, url_prefix='/api/users')


@user_profile_bp.route('/<username>', methods=['GET'])
@jwt_required()
def get_user_profile(username):
    """
    Get a user's profile with privacy-respecting data
    """
    try:
        current_user_id = int(get_jwt_identity())
        
        # Find the target user
        target_user = User.query.filter_by(username=username).first()
        if not target_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if they're friends
        are_friends = False
        if current_user_id != target_user.user_id:
            friendship = Friendship.query.filter(
                or_(
                    and_(
                        Friendship.user_id_1 == min(current_user_id, target_user.user_id),
                        Friendship.user_id_2 == max(current_user_id, target_user.user_id)
                    )
                ),
                Friendship.status == FriendshipStatus.ACCEPTED
            ).first()
            are_friends = friendship is not None
        
        # Base profile (always visible)
        profile = {
            'userId': target_user.user_id,
            'username': target_user.username,
            'displayName': target_user.display_name,
            'bio': target_user.bio,
            'isMe': current_user_id == target_user.user_id,
            'areFriends': are_friends
        }
        
        # Check privacy settings
        can_view_stats = (
            current_user_id == target_user.user_id or
            (target_user.privacy_stats == 'public') or
            (target_user.privacy_stats == 'friends' and are_friends)
        )
        
        can_view_collection = (
            current_user_id == target_user.user_id or
            (target_user.privacy_collection == 'public') or
            (target_user.privacy_collection == 'friends' and are_friends)
        )
        
        can_view_ratings = (
            current_user_id == target_user.user_id or
            (target_user.privacy_ratings == 'public') or
            (target_user.privacy_ratings == 'friends' and are_friends)
        )
        
        profile['privacy'] = {
            'canViewStats': can_view_stats,
            'canViewCollection': can_view_collection,
            'canViewRatings': can_view_ratings
        }
        
        # Add stats if allowed
        if can_view_stats:
            from src.models import MediaStatus
            total_rated = Media.query.filter_by(
                user_id=target_user.user_id,
                status=MediaStatus.WATCHED
            ).count()
            
            total_watchlist = Media.query.filter_by(
                user_id=target_user.user_id,
                status=MediaStatus.WANT_TO_WATCH
            ).count()
            
            total_friends = Friendship.query.filter(
                or_(
                    Friendship.user_id_1 == target_user.user_id,
                    Friendship.user_id_2 == target_user.user_id
                ),
                Friendship.status == FriendshipStatus.ACCEPTED
            ).count()
            
            profile['stats'] = {
                'totalRated': total_rated,
                'totalWatchlist': total_watchlist,
                'totalFriends': total_friends
            }
        
        # Add media if collection is visible
        if can_view_collection:
            media_list = Media.query.filter_by(user_id=target_user.user_id).all()
            
            # If ratings are not visible, remove rating info
            if not can_view_ratings:
                profile['media'] = [
                    {
                        'mediaId': m.media_id,
                        'title': m.title,
                        'mediaType': m.media_type.value,
                        'posterUrl': m.poster_url,
                        'releaseYear': m.release_year,
                        'status': m.status.value
                    }
                    for m in media_list
                ]
            else:
                profile['media'] = [m.to_dict(include_cast=False) for m in media_list]
        
        return jsonify(profile), 200
        
    except Exception as e:
        print(f"Error in get_user_profile: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to load user profile', 'message': str(e)}), 500