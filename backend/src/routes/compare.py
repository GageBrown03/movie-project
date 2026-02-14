# backend/src/routes/compare.py
# Comparative ratings API routes for Flask

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, User, Media, MediaStatus
from sqlalchemy import func

compare = Blueprint('compare', __name__, url_prefix='/api/compare')


# ==========================================
# Helper Functions
# ==========================================

def can_see_ratings(viewer_id, target_user_id):
    """Check if viewer can see target user's ratings"""
    # Can always see own ratings
    if viewer_id == target_user_id:
        return True
    
    target_user = User.query.get(target_user_id)
    if not target_user:
        return False
    
    # Check privacy setting
    if target_user.privacy_ratings == 'public':
        return True
    elif target_user.privacy_ratings == 'friends':
        from src.routes.friends import are_friends
        return are_friends(viewer_id, target_user_id)
    else:  # private
        return False


# ==========================================
# GET /api/compare/:username - Get comparison with a friend
# ==========================================

@compare.route('/<string:username>', methods=['GET'])
@jwt_required()
def get_comparison(username):
    """
    Get side-by-side comparison with a friend
    Returns: both users' media, ratings, and comparison stats
    """
    current_user_id = get_jwt_identity()
    
    # Get friend's user
    friend = User.query.filter_by(username=username).first()
    
    if not friend:
        return jsonify({'error': 'User not found'}), 404
    
    friend_id = friend.user_id
    
    # Check if they're friends
    from src.routes.friends import are_friends
    if not are_friends(current_user_id, friend_id):
        return jsonify({'error': 'You must be friends to compare ratings'}), 403
    
    # Check privacy permissions
    if not can_see_ratings(current_user_id, friend_id):
        return jsonify({'error': 'This user\'s ratings are private'}), 403
    
    # Get current user's media
    my_media = Media.query.filter_by(
        user_id=current_user_id,
        status=MediaStatus.WATCHED
    ).filter(Media.rating.isnot(None)).all()
    
    # Get friend's media
    friend_media = Media.query.filter_by(
        user_id=friend_id,
        status=MediaStatus.WATCHED
    ).filter(Media.rating.isnot(None)).all()
    
    # Create lookup dictionaries by TMDB ID
    my_ratings = {m.tmdb_id: m for m in my_media if m.tmdb_id}
    friend_ratings = {m.tmdb_id: m for m in friend_media if m.tmdb_id}
    
    # Find common movies (both rated)
    common_tmdb_ids = set(my_ratings.keys()) & set(friend_ratings.keys())
    
    # Build comparison data
    comparisons = []
    
    for tmdb_id in common_tmdb_ids:
        my_item = my_ratings[tmdb_id]
        friend_item = friend_ratings[tmdb_id]
        
        difference = my_item.rating - friend_item.rating
        
        comparisons.append({
            'tmdbId': tmdb_id,
            'title': my_item.title,
            'mediaType': my_item.media_type.value,
            'releaseYear': my_item.release_year,
            'posterUrl': my_item.poster_url,
            'myRating': my_item.rating,
            'friendRating': friend_item.rating,
            'difference': difference,
            'agreement': abs(difference) <= 1,  # Within 1 star = agreement
        })
    
    # Sort by biggest disagreement first
    comparisons.sort(key=lambda x: abs(x['difference']), reverse=True)
    
    # Calculate stats
    total_common = len(comparisons)
    
    if total_common > 0:
        agreements = sum(1 for c in comparisons if c['agreement'])
        agreement_rate = (agreements / total_common) * 100
        
        # Find movies you both loved (both 5 stars)
        both_loved = [c for c in comparisons if c['myRating'] == 5 and c['friendRating'] == 5]
        
        # Find biggest disagreements
        biggest_disagreements = [c for c in comparisons if abs(c['difference']) >= 3]
        
        # Find movies you loved but friend didn't (or vice versa)
        recommendations_for_friend = [
            {
                'tmdbId': m.tmdb_id, 
                'title': m.title, 
                'mediaType': m.media_type.value,  # ✅ Added
                'releaseYear': m.release_year,     # ✅ Added
                'rating': m.rating, 
                'posterUrl': m.poster_url
            }
            for m in my_media 
            if m.tmdb_id and m.tmdb_id not in friend_ratings and m.rating >= 4
        ][:10]
        
        recommendations_for_me = [
            {
                'tmdbId': m.tmdb_id, 
                'title': m.title, 
                'mediaType': m.media_type.value,  # ✅ Added
                'releaseYear': m.release_year,     # ✅ Added
                'rating': m.rating, 
                'posterUrl': m.poster_url
            }
            for m in friend_media 
            if m.tmdb_id and m.tmdb_id not in my_ratings and m.rating >= 4
        ][:10]
    else:
        agreement_rate = 0
        both_loved = []
        biggest_disagreements = []
        recommendations_for_friend = []
        recommendations_for_me = []
    
    return jsonify({
        'friend': {
            'userId': friend.user_id,
            'username': friend.username,
            'displayName': friend.display_name,
        },
        'stats': {
            'totalCommon': total_common,
            'agreementRate': round(agreement_rate, 1),
            'agreements': sum(1 for c in comparisons if c['agreement']),
            'bothLovedCount': len(both_loved),
            'myTotalRated': len(my_media),
            'friendTotalRated': len(friend_media),
        },
        'comparisons': comparisons,
        'bothLoved': both_loved[:10],
        'biggestDisagreements': biggest_disagreements[:10],
        'recommendationsForFriend': recommendations_for_friend,
        'recommendationsForMe': recommendations_for_me,
    }), 200


# ==========================================
# GET /api/compare/:username/stats - Get just stats (faster)
# ==========================================

@compare.route('/<string:username>/stats', methods=['GET'])
@jwt_required()
def get_comparison_stats(username):
    """
    Get just the comparison stats without full data
    Faster endpoint for displaying summary
    """
    current_user_id = get_jwt_identity()
    
    # Get friend's user
    friend = User.query.filter_by(username=username).first()
    
    if not friend:
        return jsonify({'error': 'User not found'}), 404
    
    friend_id = friend.user_id
    
    # Check if they're friends
    from src.routes.friends import are_friends
    if not are_friends(current_user_id, friend_id):
        return jsonify({'error': 'You must be friends to compare ratings'}), 403
    
    # Check privacy
    if not can_see_ratings(current_user_id, friend_id):
        return jsonify({'error': 'This user\'s ratings are private'}), 403
    
    # Count common movies (using raw SQL for performance)
    from sqlalchemy import text
    
    query = text("""
        SELECT COUNT(*) as total_common,
               SUM(CASE WHEN ABS(m1.rating - m2.rating) <= 1 THEN 1 ELSE 0 END) as agreements
        FROM media m1
        JOIN media m2 ON m1.tmdb_id = m2.tmdb_id
        WHERE m1.user_id = :user1_id
          AND m2.user_id = :user2_id
          AND m1.status = 'watched'
          AND m2.status = 'watched'
          AND m1.rating IS NOT NULL
          AND m2.rating IS NOT NULL
          AND m1.tmdb_id IS NOT NULL
    """)
    
    result = db.session.execute(query, {
        'user1_id': current_user_id,
        'user2_id': friend_id
    }).fetchone()
    
    total_common = result[0] or 0
    agreements = result[1] or 0
    
    agreement_rate = (agreements / total_common * 100) if total_common > 0 else 0
    
    # Get total rated counts
    my_total = Media.query.filter_by(
        user_id=current_user_id,
        status=MediaStatus.WATCHED
    ).filter(Media.rating.isnot(None)).count()
    
    friend_total = Media.query.filter_by(
        user_id=friend_id,
        status=MediaStatus.WATCHED
    ).filter(Media.rating.isnot(None)).count()
    
    return jsonify({
        'friend': {
            'userId': friend.user_id,
            'username': friend.username,
            'displayName': friend.display_name,
        },
        'stats': {
            'totalCommon': total_common,
            'agreementRate': round(agreement_rate, 1),
            'agreements': agreements,
            'myTotalRated': my_total,
            'friendTotalRated': friend_total,
        }
    }), 200