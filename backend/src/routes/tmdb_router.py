from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
import requests
import os

tmdb_router = Blueprint('tmdb', __name__, url_prefix='/tmdb')

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p'


@tmdb_router.get('/search')
@jwt_required()
def search_movies():
    """
    Search TMDB for movies
    Query params: ?query=interstellar
    """
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    if not TMDB_API_KEY:
        return jsonify({'error': 'TMDB API key not configured'}), 500
    
    try:
        # Search TMDB
        response = requests.get(
            f'{TMDB_BASE_URL}/search/movie',
            params={
                'api_key': TMDB_API_KEY,
                'query': query,
                'include_adult': False,
                'language': 'en-US',
                'page': 1
            },
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        
        # Transform results to our format
        results = []
        for movie in data.get('results', [])[:10]:  # Limit to top 10
            results.append({
                'tmdbId': movie.get('id'),
                'title': movie.get('title'),
                'releaseYear': movie.get('release_date', '')[:4] if movie.get('release_date') else None,
                'plot': movie.get('overview'),
                'posterUrl': f"{TMDB_IMAGE_BASE}/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                'backdropUrl': f"{TMDB_IMAGE_BASE}/w1280{movie['backdrop_path']}" if movie.get('backdrop_path') else None,
                'tmdbRating': movie.get('vote_average'),
            })
        
        return jsonify(results), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'TMDB API error: {str(e)}'}), 500


@tmdb_router.get('/movie/<int:tmdb_id>')
@jwt_required()
def get_movie_details(tmdb_id):
    """
    Get full details for a specific TMDB movie
    Includes: credits (director), runtime, genres, ratings
    """
    if not TMDB_API_KEY:
        return jsonify({'error': 'TMDB API key not configured'}), 500
    
    try:
        # Get movie details
        response = requests.get(
            f'{TMDB_BASE_URL}/movie/{tmdb_id}',
            params={
                'api_key': TMDB_API_KEY,
                'append_to_response': 'credits,external_ids',  # Get director and IMDB ID
                'language': 'en-US'
            },
            timeout=5
        )
        response.raise_for_status()
        movie = response.json()
        
        # Extract director from credits
        director = None
        if 'credits' in movie and 'crew' in movie['credits']:
            directors = [p['name'] for p in movie['credits']['crew'] if p['job'] == 'Director']
            director = directors[0] if directors else None
        
        # Get IMDB ID
        imdb_id = movie.get('external_ids', {}).get('imdb_id')
        
        # Format genres
        genres = ','.join([g['name'] for g in movie.get('genres', [])])
        
        result = {
            'tmdbId': movie.get('id'),
            'title': movie.get('title'),
            'director': director,
            'releaseYear': movie.get('release_date', '')[:4] if movie.get('release_date') else None,
            'runtime': movie.get('runtime'),
            'plot': movie.get('overview'),
            'genres': genres,
            'posterUrl': f"{TMDB_IMAGE_BASE}/w500{movie['poster_path']}" if movie.get('poster_path') else None,
            'backdropUrl': f"{TMDB_IMAGE_BASE}/original{movie['backdrop_path']}" if movie.get('backdrop_path') else None,
            'tmdbRating': movie.get('vote_average'),
            'imdbId': imdb_id,
        }
        
        # If we have IMDB ID, we could fetch IMDB rating here
        # For now, TMDB rating is good enough (it's an average of multiple sources)
        
        return jsonify(result), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'TMDB API error: {str(e)}'}), 500