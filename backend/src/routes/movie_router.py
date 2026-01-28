from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import Movie, db

movie_router = Blueprint('movies', __name__, url_prefix='/movies')


@movie_router.get('')
@jwt_required()  # NEW: Must be logged in
def get_all_movies():
    """Get all movies for the current user"""
    user_id = get_jwt_identity()  # NEW: Get current user's ID
    movies = Movie.query.filter_by(user_id=user_id).all()  # NEW: Filter by user
    return jsonify([m.to_dict() for m in movies])


@movie_router.get('/<int:movie_id>')
@jwt_required()  # NEW: Must be logged in
def get_single_movie(movie_id: int):
    """Get a single movie (only if it belongs to current user)"""
    user_id = get_jwt_identity()
    movie = Movie.query.filter_by(movie_id=movie_id, user_id=user_id).first()  # NEW: Check ownership
    
    if not movie:
        abort(404)
    
    return jsonify(movie.to_dict())


@movie_router.post('')
@jwt_required()  # NEW: Must be logged in
def create_movie():
    """Create a new movie for the current user"""
    try:
        user_id = get_jwt_identity()  # NEW: Get current user's ID
        data = request.get_json()
        
        # Validate required fields
        title = data.get('title', '').strip()
        director = data.get('director', '').strip()
        rating = data.get('rating')
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        if not director:
            return jsonify({'error': 'Director is required'}), 400
        
        # Validate rating
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1-5'}), 400
        except (TypeError, ValueError):
            return jsonify({'error': 'Rating must be a number'}), 400
        
        # NEW: Pass user_id when creating movie
        new_movie = Movie(
            title=title,
            director=director,
            rating=rating,
            user_id=user_id,
            description=data.get('description'),
            image_url=data.get('imageUrl')
        )
        db.session.add(new_movie)
        db.session.commit()
        
        return jsonify(new_movie.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@movie_router.patch('/<int:movie_id>')
@jwt_required()  # NEW: Must be logged in
def update_movie(movie_id: int):
    """Update a movie (only if it belongs to current user)"""
    user_id = get_jwt_identity()
    movie_obj = Movie.query.filter_by(movie_id=movie_id, user_id=user_id).first()  # NEW: Check ownership
    
    if not movie_obj:
        return jsonify({'error': 'Movie not found or unauthorized'}), 404
    
    data = request.get_json()
    
    # Only update fields that are provided
    if 'title' in data:
        movie_obj.title = data['title']
    if 'director' in data:
        movie_obj.director = data['director']
    if 'rating' in data:
        rating = int(data['rating'])
        if 1 <= rating <= 5:
            movie_obj.rating = rating
    if 'description' in data:
        movie_obj.description = data['description']
    if 'imageUrl' in data:
        movie_obj.image_url = data['imageUrl']
    
    db.session.commit()
    return jsonify(movie_obj.to_dict())


@movie_router.delete('/<int:movie_id>')
@jwt_required()  # NEW: Must be logged in
def delete_movie(movie_id: int):
    """Delete a movie (only if it belongs to current user)"""
    user_id = get_jwt_identity()
    existing_movie = Movie.query.filter_by(movie_id=movie_id, user_id=user_id).first()  # NEW: Check ownership
    
    if not existing_movie:
        return jsonify({'error': 'Movie not found or unauthorized'}), 404
    
    db.session.delete(existing_movie)
    db.session.commit()
    return jsonify(existing_movie.to_dict())