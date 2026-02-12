from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, Media, MediaType, MediaStatus, Activity
from src.routes.activity_routes import create_activity
from src.utils.actor_utils import add_cast_to_media

media_router = Blueprint('media', __name__, url_prefix='/media')


@media_router.get('')
@jwt_required()
def get_all_media():
    """
    Get all media (movies + TV shows) for the current user.
    
    Query params:
        - type: Filter by media type ('movie' or 'tv')
        - status: Filter by status ('watched', 'want_to_watch', 'watching')
    """
    user_id = int(get_jwt_identity())
    
    # Start with base query
    query = Media.query.filter_by(user_id=user_id)
    
    # Apply filters
    media_type = request.args.get('type')
    if media_type:
        try:
            query = query.filter_by(media_type=MediaType(media_type))
        except ValueError:
            return jsonify({'error': 'Invalid media type'}), 400
    
    status = request.args.get('status')
    if status:
        try:
            query = query.filter_by(status=MediaStatus(status))
        except ValueError:
            return jsonify({'error': 'Invalid status'}), 400
    
    # Execute query
    media_list = query.all()
    
    # Return with cast included
    return jsonify([m.to_dict(include_cast=True) for m in media_list])


@media_router.get('/<int:media_id>')
@jwt_required()
def get_single_media(media_id: int):
    """Get a single media item (only if it belongs to current user)"""
    user_id = int(get_jwt_identity())
    media = Media.query.filter_by(media_id=media_id, user_id=user_id).first()
    
    if not media:
        abort(404)
    
    return jsonify(media.to_dict(include_cast=True))


@media_router.post('')
@jwt_required()
def create_media():
    """
    Create a new media entry for the current user.
    
    Request body should include:
        - title (required)
        - media_type (required): 'movie' or 'tv'
        - status (required): 'watched' or 'want_to_watch'
        - rating (required if status='watched'): 1-5
        - cast (optional): Array of cast data from TMDB
        - All other media fields (optional)
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validate required fields
        title = data.get('title', '').strip()
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        # Validate media type
        media_type_str = data.get('media_type', '').lower()
        try:
            media_type = MediaType(media_type_str)
        except ValueError:
            return jsonify({'error': 'Invalid media_type. Must be "movie" or "tv"'}), 400
        
        # Validate status
        status_str = data.get('status', 'watched').lower()
        try:
            status = MediaStatus(status_str)
        except ValueError:
            return jsonify({'error': 'Invalid status'}), 400
        
        # Validate rating based on status
        rating = data.get('rating')
        if status == MediaStatus.WATCHED:
            if rating is None:
                return jsonify({'error': 'Rating is required for watched media'}), 400
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    return jsonify({'error': 'Rating must be between 1-5'}), 400
            except (TypeError, ValueError):
                return jsonify({'error': 'Rating must be a number'}), 400
        else:
            # Watchlist items should not have ratings
            rating = None
        
        # Build media object with common fields
        media_data = {
            'title': title,
            'media_type': media_type,
            'user_id': user_id,
            'status': status,
            'rating': rating,
        }
        
        # Add optional common fields
        optional_fields = [
            'release_year', 'plot', 'genres', 'tmdb_id',
            'poster_url', 'backdrop_url', 'tmdb_rating', 'imdb_rating',
            'watched_date', 'notes'
        ]
        
        for field in optional_fields:
            if field in data and data[field] is not None:
                media_data[field] = data[field]
        
        # Add movie-specific fields
        if media_type == MediaType.MOVIE:
            if 'director' in data:
                media_data['director'] = data['director']
            if 'runtime' in data:
                media_data['runtime'] = data['runtime']
        
        # Add TV-specific fields
        elif media_type == MediaType.TV:
            tv_fields = ['number_of_seasons', 'number_of_episodes', 'show_status', 'seasons_watched']
            for field in tv_fields:
                if field in data and data[field] is not None:
                    media_data[field] = data[field]
        
        # Create media entry
        new_media = Media(**media_data)
        db.session.add(new_media)
        db.session.flush()  # Get media_id before adding cast
        
        # Add cast if provided
        if 'cast' in data and data['cast']:
            add_cast_to_media(new_media.media_id, data['cast'])
        
        db.session.commit()
        
        # ACTIVITY TRACKING: Create activity for this addition
        activity_type = 'rating' if new_media.status == MediaStatus.WATCHED else 'watchlist'
        create_activity(
            user_id=user_id,
            activity_type=activity_type,
            media_id=new_media.media_id,
            metadata={'rating': new_media.rating} if new_media.rating else None
        )
        
        return jsonify(new_media.to_dict(include_cast=True)), 201  
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating media: {str(e)}")
        return jsonify({'error': str(e)}), 500


@media_router.patch('/<int:media_id>')
@jwt_required()
def update_media(media_id: int):
    """Update a media entry (only if it belongs to current user)"""
    user_id = int(get_jwt_identity())
    media = Media.query.filter_by(media_id=media_id, user_id=user_id).first()
    
    if not media:
        return jsonify({'error': 'Media not found or unauthorized'}), 404
    
    data = request.get_json()
    
    # Map of camelCase frontend keys to snake_case db fields
    field_map = {
        'title': 'title',
        'status': 'status',
        'rating': 'rating',
        'director': 'director',
        'releaseYear': 'release_year',
        'runtime': 'runtime',
        'plot': 'plot',
        'genres': 'genres',
        'tmdbId': 'tmdb_id',
        'posterUrl': 'poster_url',
        'backdropUrl': 'backdrop_url',
        'imdbRating': 'imdb_rating',
        'tmdbRating': 'tmdb_rating',
        'watchedDate': 'watched_date',
        'notes': 'notes',
        'numberOfSeasons': 'number_of_seasons',
        'numberOfEpisodes': 'number_of_episodes',
        'showStatus': 'show_status',
        'seasonsWatched': 'seasons_watched',
    }
    
    # Handle status change
    if 'status' in data:
        try:
            new_status = MediaStatus(data['status'])
            media.status = new_status
            
            # If moving to WATCHED, rating is required
            if new_status == MediaStatus.WATCHED and not data.get('rating') and not media.rating:
                return jsonify({'error': 'Rating required when marking as watched'}), 400
            
            # If moving to WANT_TO_WATCH, clear rating
            if new_status == MediaStatus.WANT_TO_WATCH:
                media.rating = None
        except ValueError:
            return jsonify({'error': 'Invalid status'}), 400
    
    # Update other fields
    for frontend_key, db_key in field_map.items():
        if frontend_key in data and frontend_key != 'status':  # Already handled status
            setattr(media, db_key, data[frontend_key])
    
    db.session.commit()
    
    # ACTIVITY TRACKING: If rating was added/changed, create activity
    if 'rating' in data and data['rating'] is not None:
        create_activity(
            user_id=user_id,
            activity_type='rating',
            media_id=media.media_id,
            metadata={'rating': media.rating}
        )
    
    return jsonify(media.to_dict(include_cast=True))


@media_router.delete('/<int:media_id>')
@jwt_required()
def delete_media(media_id: int):
    """Delete a media entry (only if it belongs to current user)"""
    user_id = int(get_jwt_identity())
    existing_media = Media.query.filter_by(media_id=media_id, user_id=user_id).first()
    
    if not existing_media:
        return jsonify({'error': 'Media not found or unauthorized'}), 404
    
    # FIXED: Delete all activities related to this media
    Activity.query.filter_by(media_id=media_id).delete()
    
    # Delete the media
    db.session.delete(existing_media)
    db.session.commit()
    
    return jsonify(existing_media.to_dict())