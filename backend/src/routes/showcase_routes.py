# backend/src/routes/showcase_routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from src.models import db, User, Media, UserShowcase, ShowcaseCategory

showcase_bp = Blueprint('showcase', __name__, url_prefix='/api/showcase')

CATEGORY_LIMITS = {
    ShowcaseCategory.TOP_MOVIES:  5,
    ShowcaseCategory.TOP_TV:      5,
    ShowcaseCategory.FAV_SERIES:  5,
    ShowcaseCategory.HIDDEN_GEM:  1,
}


def _serialize_showcase(entries):
    """Group entries by category and return structured dict."""
    result = {
        'topMovies':  [],
        'topTv':      [],
        'favSeries':  [],
        'hiddenGem':  None,
    }
    key_map = {
        'top_movies': 'topMovies',
        'top_tv':     'topTv',
        'fav_series': 'favSeries',
        'hidden_gem': 'hiddenGem',
    }
    for entry in sorted(entries, key=lambda e: e.rank):
        key = key_map.get(entry.category.value)
        if key == 'hiddenGem':
            result['hiddenGem'] = entry.to_dict()
        elif key:
            result[key].append(entry.to_dict())
    return result


@showcase_bp.route('/<username>', methods=['GET'])
def get_public_showcase(username):
    """
    Public endpoint — returns showcase if the viewer has canViewRatings access.
    Respects privacy settings: showcase is gated behind privacy_ratings.
    """
    user = User.query.filter_by(username=username).first_or_404()

    # Determine viewer identity (optional JWT)
    viewer_id = None
    try:
        verify_jwt_in_request(optional=True)
        from flask_jwt_extended import get_jwt_identity
        viewer_id = get_jwt_identity()
        if viewer_id:
            viewer_id = int(viewer_id)
    except Exception:
        pass

    is_own_profile = viewer_id == user.user_id

    # Privacy gate — mirrors canViewRatings logic
    if not is_own_profile and user.privacy_ratings == 'private':
        return jsonify({'showcase': None, 'reason': 'private'}), 200

    # Friends-only check
    if not is_own_profile and user.privacy_ratings == 'friends':
        if not viewer_id:
            return jsonify({'showcase': None, 'reason': 'friends_only'}), 200
        from src.models import Friendship, FriendshipStatus
        uid1, uid2 = (min(viewer_id, user.user_id), max(viewer_id, user.user_id))
        friendship = Friendship.query.filter_by(
            user_id_1=uid1, user_id_2=uid2, status=FriendshipStatus.ACCEPTED
        ).first()
        if not friendship:
            return jsonify({'showcase': None, 'reason': 'friends_only'}), 200

    entries = UserShowcase.query.filter_by(user_id=user.user_id).all()
    return jsonify({
        'showcase': _serialize_showcase(entries),
        'isOwn': is_own_profile,
    }), 200


@showcase_bp.route('/mine', methods=['GET'])
@jwt_required()
def get_own_showcase():
    """Returns the authenticated user's showcase with full edit metadata."""
    user_id = int(get_jwt_identity())
    entries = UserShowcase.query.filter_by(user_id=user_id).all()
    return jsonify({
        'showcase': _serialize_showcase(entries),
        'isOwn': True,
    }), 200


@showcase_bp.route('', methods=['PUT'])
@jwt_required()
def save_showcase():
    """
    Replace the user's entire showcase in one atomic operation.
    Payload shape:
    {
      "topMovies":  [{ "mediaId": 5, "rank": 1 }, ...],   // up to 5
      "topTv":      [{ "mediaId": 7, "rank": 1 }, ...],   // up to 5
      "favSeries":  [                                      // up to 5
          { "mediaId": 3, "rank": 1,
            "tmdbCollectionId": 131295,
            "tmdbCollectionName": "The Bourne Collection" },
          ...
      ],
      "hiddenGem":  { "mediaId": 12, "rank": 1, "note": "Changed my life" }  // nullable
    }
    Any key can be omitted to leave that category unchanged.
    Send an empty array / null to clear a category.
    """
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    category_map = {
        'topMovies':  ShowcaseCategory.TOP_MOVIES,
        'topTv':      ShowcaseCategory.TOP_TV,
        'favSeries':  ShowcaseCategory.FAV_SERIES,
        'hiddenGem':  ShowcaseCategory.HIDDEN_GEM,
    }

    for key, category in category_map.items():
        if key not in data:
            continue  # not in payload — leave untouched

        # Delete existing entries for this category
        UserShowcase.query.filter_by(user_id=user_id, category=category).delete()

        raw = data[key]
        if not raw:  # null or [] clears the category
            continue

        # Normalise: hiddenGem is a single object, others are arrays
        items = [raw] if isinstance(raw, dict) else raw
        limit = CATEGORY_LIMITS[category]

        for item in items[:limit]:
            media_id = item.get('mediaId')
            rank = item.get('rank', 1)

            # Verify media belongs to this user (if provided)
            if media_id:
                media = Media.query.filter_by(
                    media_id=media_id, user_id=user_id
                ).first()
                if not media:
                    continue  # silently skip invalid media_ids

            entry = UserShowcase(
                user_id=user_id,
                category=category,
                rank=rank,
                media_id=media_id,
                tmdb_collection_id=item.get('tmdbCollectionId'),
                tmdb_collection_name=item.get('tmdbCollectionName'),
                note=item.get('note'),
            )
            db.session.add(entry)

    db.session.commit()

    # Return updated showcase
    entries = UserShowcase.query.filter_by(user_id=user_id).all()
    return jsonify({
        'showcase': _serialize_showcase(entries),
        'isOwn': True,
    }), 200