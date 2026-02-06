from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import Movie, db

movie_router = Blueprint('movies', __name__, url_prefix='/movies')


@movie_router.get('')
@jwt_required()
def get_all_movies():
    """Get all movies for the current user"""
    user_id = int(get_jwt_identity())
    movies = Movie.query.filter_by(user_id=user_id).all()
    return jsonify([m.to_dict() for m in movies])


@movie_router.get('/<int:movie_id>')
@jwt_required()
def get_single_movie(movie_id: int):
    """Get a single movie (only if it belongs to current user)"""
    user_id = int(get_jwt_identity())
    movie = Movie.query.filter_by(movie_id=movie_id, user_id=user_id).first()
    
    if not movie:
        abort(404)
    
    return jsonify(movie.to_dict())


@movie_router.post('')
@jwt_required()
def create_movie():
    """Create a new movie for the current user"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validate required fields
        title = data.get('title', '').strip()
        rating = data.get('rating')
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        # Validate rating
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1-5'}), 400
        except (TypeError, ValueError):
            return jsonify({'error': 'Rating must be a number'}), 400
        
        # Build movie with all optional TMDB fields
        movie_data = {
            'title': title,
            'rating': rating,
            'user_id': user_id,
        }
        
        # Add optional fields if provided
        optional_fields = [
            'director', 'release_year', 'runtime', 'plot', 'genres',
            'tmdb_id', 'poster_url', 'backdrop_url',
            'imdb_rating', 'tmdb_rating', 'watched_date', 'notes'
        ]
        
        for field in optional_fields:
            # Convert camelCase from frontend to snake_case
            camel_field = ''.join(['_' + c.lower() if c.isupper() else c for c in field]).lstrip('_')
            if camel_field in data and data[camel_field] is not None:
                movie_data[field] = data[camel_field]
        
        new_movie = Movie(**movie_data)
        db.session.add(new_movie)
        db.session.commit()
        
        return jsonify(new_movie.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating movie: {str(e)}")  # Debug
        return jsonify({'error': str(e)}), 500


@movie_router.patch('/<int:movie_id>')
@jwt_required()
def update_movie(movie_id: int):
    """Update a movie (only if it belongs to current user)"""
    user_id = int(get_jwt_identity())
    movie_obj = Movie.query.filter_by(movie_id=movie_id, user_id=user_id).first()
    
    if not movie_obj:
        return jsonify({'error': 'Movie not found or unauthorized'}), 404
    
    data = request.get_json()
    
    # Map of camelCase frontend keys to snake_case db fields
    field_map = {
        'title': 'title',
        'director': 'director',
        'releaseYear': 'release_year',
        'runtime': 'runtime',
        'plot': 'plot',
        'genres': 'genres',
        'rating': 'rating',
        'tmdbId': 'tmdb_id',
        'posterUrl': 'poster_url',
        'backdropUrl': 'backdrop_url',
        'imdbRating': 'imdb_rating',
        'tmdbRating': 'tmdb_rating',
        'watchedDate': 'watched_date',
        'notes': 'notes',
    }
    
    for frontend_key, db_key in field_map.items():
        if frontend_key in data:
            setattr(movie_obj, db_key, data[frontend_key])
    
    db.session.commit()
    return jsonify(movie_obj.to_dict())


@movie_router.delete('/<int:movie_id>')
@jwt_required()
def delete_movie(movie_id: int):
    """Delete a movie (only if it belongs to current user)"""
    user_id = int(get_jwt_identity())
    existing_movie = Movie.query.filter_by(movie_id=movie_id, user_id=user_id).first()
    
    if not existing_movie:
        return jsonify({'error': 'Movie not found or unauthorized'}), 404
    
    db.session.delete(existing_movie)
    db.session.commit()
    return jsonify(existing_movie.to_dict())