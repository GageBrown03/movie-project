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
def search_multi():
    """
    Search TMDB for both movies AND TV shows simultaneously.
    Query params: ?query=breaking bad
    
    Returns unified results with type distinction (movie vs tv).
    """
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    if not TMDB_API_KEY:
        return jsonify({'error': 'TMDB API key not configured'}), 500
    
    try:
        # Use TMDB's multi-search endpoint (searches movies + TV simultaneously)
        response = requests.get(
            f'{TMDB_BASE_URL}/search/multi',
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
        for item in data.get('results', [])[:15]:  # Top 15 results
            media_type = item.get('media_type')
            
            # Skip person results (we only want movies & TV)
            if media_type not in ['movie', 'tv']:
                continue
            
            # Common fields
            result = {
                'tmdbId': item.get('id'),
                'mediaType': media_type,
                'plot': item.get('overview'),
                'posterUrl': f"{TMDB_IMAGE_BASE}/w500{item['poster_path']}" if item.get('poster_path') else None,
                'backdropUrl': f"{TMDB_IMAGE_BASE}/w1280{item['backdrop_path']}" if item.get('backdrop_path') else None,
                'tmdbRating': item.get('vote_average'),
            }
            
            # Movie-specific fields
            if media_type == 'movie':
                result['title'] = item.get('title')
                result['releaseYear'] = item.get('release_date', '')[:4] if item.get('release_date') else None
            
            # TV-specific fields
            elif media_type == 'tv':
                result['title'] = item.get('name')
                result['releaseYear'] = item.get('first_air_date', '')[:4] if item.get('first_air_date') else None
            
            results.append(result)
        
        return jsonify(results), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'TMDB API error: {str(e)}'}), 500


@tmdb_router.get('/movie/<int:tmdb_id>')
@jwt_required()
def get_movie_details(tmdb_id):
    """
    Get full details for a specific TMDB movie.
    Includes: credits (director + cast), runtime, genres, ratings, external IDs.
    """
    if not TMDB_API_KEY:
        return jsonify({'error': 'TMDB API key not configured'}), 500
    
    try:
        # Get movie details with credits
        response = requests.get(
            f'{TMDB_BASE_URL}/movie/{tmdb_id}',
            params={
                'api_key': TMDB_API_KEY,
                'append_to_response': 'credits,external_ids',
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
        
        # Extract cast (top 10 for storage)
        cast = []
        if 'credits' in movie and 'cast' in movie['credits']:
            cast = movie['credits']['cast'][:10]
        
        # Get IMDB ID
        imdb_id = movie.get('external_ids', {}).get('imdb_id')
        
        # Format genres
        genres = ','.join([g['name'] for g in movie.get('genres', [])])
        
        result = {
            'tmdbId': movie.get('id'),
            'mediaType': 'movie',
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
            'cast': cast  # Raw TMDB cast data
        }
        
        return jsonify(result), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'TMDB API error: {str(e)}'}), 500


@tmdb_router.get('/tv/<int:tmdb_id>')
@jwt_required()
def get_tv_details(tmdb_id):
    """
    Get full details for a specific TMDB TV show.
    Includes: credits (creators + cast), seasons, episodes, status, genres, ratings.
    """
    if not TMDB_API_KEY:
        return jsonify({'error': 'TMDB API key not configured'}), 500
    
    try:
        # Get TV show details with credits
        response = requests.get(
            f'{TMDB_BASE_URL}/tv/{tmdb_id}',
            params={
                'api_key': TMDB_API_KEY,
                'append_to_response': 'credits,external_ids',
                'language': 'en-US'
            },
            timeout=5
        )
        response.raise_for_status()
        show = response.json()
        
        # Extract creators (TV equivalent of director)
        creators = []
        if show.get('created_by'):
            creators = [c['name'] for c in show['created_by']]
        director = ', '.join(creators) if creators else None
        
        # Extract cast (top 10 for storage)
        cast = []
        if 'credits' in show and 'cast' in show['credits']:
            cast = show['credits']['cast'][:10]
        
        # Get external IDs
        imdb_id = show.get('external_ids', {}).get('imdb_id')
        
        # Format genres
        genres = ','.join([g['name'] for g in show.get('genres', [])])
        
        result = {
            'tmdbId': show.get('id'),
            'mediaType': 'tv',
            'title': show.get('name'),
            'director': director,  # Actually creators, but stored in same field
            'releaseYear': show.get('first_air_date', '')[:4] if show.get('first_air_date') else None,
            'plot': show.get('overview'),
            'genres': genres,
            'posterUrl': f"{TMDB_IMAGE_BASE}/w500{show['poster_path']}" if show.get('poster_path') else None,
            'backdropUrl': f"{TMDB_IMAGE_BASE}/original{show['backdrop_path']}" if show.get('backdrop_path') else None,
            'tmdbRating': show.get('vote_average'),
            'imdbId': imdb_id,
            'numberOfSeasons': show.get('number_of_seasons'),
            'numberOfEpisodes': show.get('number_of_episodes'),
            'showStatus': show.get('status'),  # "Returning Series", "Ended", "Canceled"
            'cast': cast  # Raw TMDB cast data
        }
        
        return jsonify(result), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'TMDB API error: {str(e)}'}), 500