from flask import Blueprint, abort, jsonify, request
from src.models import movie, db

movie_router = Blueprint('movies', __name__, url_prefix='/movies')


@movie_router.get('')
def get_all_movies():
    movies = movie.query.all()
    return jsonify([movie.to_dict() for movie in movies])



@movie_router.get('/<int:movie_id>')
def get_single_movie(movie_id: int):
    movie = movie.query.get(movie_id)
    if not movie:
        abort(404)
    movie_as_dict = movie.to_dict()
    return jsonify(movie_as_dict)

@movie_router.post('')
def create_movie():
    title = request.json.get('title')
    director = request.json.get('director')
    rating = request.json.get('rating')

    if not title or not director or not rating or rating < 1 or rating > 5:
        abort(400)

    new_movie = movie(title, director, rating)
    db.session.add(new_movie)
    db.session.commit()

    return jsonify(new_movie.to_dict()), 201

@movie_router.put('/<int:movie_id>')
def update_movie(movie_id: int):
    
    title = request.json.get('title')
    director = request.json.get('director')
    rating = request.json.get('rating')

    if not title or not director or not rating or rating < 1 or rating > 5:
        abort(400)

    existing_movie = movie.query.get_or_404(movie_id)
    existing_movie.title = title
    existing_movie.director = director
    existing_movie.rating = rating
    db.session.commit()

    return None, 204


@movie_router.delete('/<int:movie_id>')
def delete_movie(movie_id: int):
    existing_movie = movie.query.get_or_404(movie_id)
    db.session.remove(existing_movie)
    db.session.commit()
    return jsonify(existing_movie.to_dict())