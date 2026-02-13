# backend/src/routes/analytics.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Media
from sqlalchemy import func
import requests
import os

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

@analytics_bp.route('/top-people', methods=['GET'])
@jwt_required()
def get_top_people():
    """
    Get top actors and directors with photos
    No time dependency - based on all-time collection
    """
    user_id = get_jwt_identity()
    
    # Get all user's media
    media_list = Media.query.filter_by(user_id=user_id).all()
    
    # Count actors
    actor_counts = {}
    for media in media_list:
        if media.cast:
            for cast_member in media.cast:
                actor_id = cast_member.get('actorId') or cast_member.get('actor_id')
                actor_name = cast_member.get('name')
                
                if actor_id and actor_name:
                    if actor_id not in actor_counts:
                        actor_counts[actor_id] = {
                            'id': actor_id,
                            'name': actor_name,
                            'count': 0
                        }
                    actor_counts[actor_id]['count'] += 1
    
    # Count directors
    director_counts = {}
    for media in media_list:
        if media.director:
            # Handle both string and object director
            if isinstance(media.director, str):
                # Simple string director name
                director_name = media.director
                # Create a simple key from name
                director_key = director_name.lower().replace(' ', '_')
                
                if director_key not in director_counts:
                    director_counts[director_key] = {
                        'id': None,
                        'name': director_name,
                        'count': 0
                    }
                director_counts[director_key]['count'] += 1
            elif isinstance(media.director, dict):
                # Director object with ID
                director_id = media.director.get('id')
                director_name = media.director.get('name')
                
                if director_id and director_name:
                    if director_id not in director_counts:
                        director_counts[director_id] = {
                            'id': director_id,
                            'name': director_name,
                            'count': 0
                        }
                    director_counts[director_id]['count'] += 1
    
    # Sort and get top 10
    top_actors = sorted(actor_counts.values(), key=lambda x: x['count'], reverse=True)[:10]
    top_directors = sorted(director_counts.values(), key=lambda x: x['count'], reverse=True)[:10]
    
    # Fetch photos from TMDB for actors
    for actor in top_actors:
        if actor['id']:
            try:
                response = requests.get(
                    f"{TMDB_BASE_URL}/person/{actor['id']}?api_key={TMDB_API_KEY}"
                )
                if response.ok:
                    data = response.json()
                    actor['photo'] = f"https://image.tmdb.org/t/p/w185{data['profile_path']}" if data.get('profile_path') else None
                else:
                    actor['photo'] = None
            except:
                actor['photo'] = None
        else:
            actor['photo'] = None
    
    # Fetch photos from TMDB for directors
    for director in top_directors:
        if director['id']:
            try:
                response = requests.get(
                    f"{TMDB_BASE_URL}/person/{director['id']}?api_key={TMDB_API_KEY}"
                )
                if response.ok:
                    data = response.json()
                    director['photo'] = f"https://image.tmdb.org/t/p/w185{data['profile_path']}" if data.get('profile_path') else None
                else:
                    director['photo'] = None
            except:
                director['photo'] = None
        else:
            director['photo'] = None
    
    return jsonify({
        'actors': top_actors,
        'directors': top_directors
    })


@analytics_bp.route('/decades', methods=['GET'])
@jwt_required()
def get_decade_preferences():
    """
    Analyze preferences by decade (using release years)
    No time dependency - based on movie release dates
    """
    user_id = get_jwt_identity()
    
    media_list = Media.query.filter_by(user_id=user_id).all()
    
    decade_counts = {}
    decade_ratings = {}
    
    for media in media_list:
        if media.release_year:
            # Calculate decade (1990s, 2000s, etc.)
            decade = (media.release_year // 10) * 10
            decade_label = f"{decade}s"
            
            if decade_label not in decade_counts:
                decade_counts[decade_label] = {
                    'decade': decade,
                    'label': decade_label,
                    'count': 0,
                    'ratings': []
                }
            
            decade_counts[decade_label]['count'] += 1
            
            # Track ratings for average
            if media.rating:
                decade_counts[decade_label]['ratings'].append(media.rating)
    
    # Calculate averages and sort
    decades = []
    for decade_data in decade_counts.values():
        ratings = decade_data['ratings']
        avg_rating = sum(ratings) / len(ratings) if ratings else None
        
        decades.append({
            'decade': decade_data['decade'],
            'label': decade_data['label'],
            'count': decade_data['count'],
            'averageRating': round(avg_rating, 1) if avg_rating else None
        })
    
    # Sort by decade (oldest to newest)
    decades.sort(key=lambda x: x['decade'])
    
    # Find favorite decade (most watched)
    favorite = max(decades, key=lambda x: x['count']) if decades else None
    
    return jsonify({
        'decades': decades,
        'favorite': favorite
    })


@analytics_bp.route('/records', methods=['GET'])
@jwt_required()
def get_all_time_records():
    """
    Get all-time personal records
    No time dependency - based on all-time data
    """
    user_id = get_jwt_identity()
    
    media_list = Media.query.filter_by(user_id=user_id).all()
    watched = [m for m in media_list if m.status == 'watched']
    rated = [m for m in media_list if m.rating]
    
    records = {}
    
    # Highest rated movie
    if rated:
        highest_rated = max(rated, key=lambda x: (x.rating, x.tmdb_rating or 0))
        records['highestRated'] = {
            'title': highest_rated.title,
            'rating': highest_rated.rating,
            'mediaId': highest_rated.media_id,
            'posterUrl': highest_rated.poster_url
        }
    
    # Lowest rated movie
    if rated:
        lowest_rated = min(rated, key=lambda x: (x.rating, -(x.tmdb_rating or 0)))
        records['lowestRated'] = {
            'title': lowest_rated.title,
            'rating': lowest_rated.rating,
            'mediaId': lowest_rated.media_id,
            'posterUrl': lowest_rated.poster_url
        }
    
    # Genre champion (most watched in one genre)
    genre_counts = {}
    for media in media_list:
        if media.genres:
            genres = media.genres if isinstance(media.genres, list) else media.genres.split(', ')
            for genre in genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    if genre_counts:
        champion_genre = max(genre_counts.items(), key=lambda x: x[1])
        records['genreChampion'] = {
            'genre': champion_genre[0],
            'count': champion_genre[1]
        }
    
    # TMDB Contrarian (biggest average difference from TMDB ratings)
    media_with_both = [m for m in rated if m.tmdb_rating]
    if media_with_both:
        diffs = []
        for m in media_with_both:
            # Convert TMDB 10-point to 5-point
            tmdb_5point = m.tmdb_rating / 2
            diff = m.rating - tmdb_5point
            diffs.append(diff)
        
        avg_diff = sum(diffs) / len(diffs)
        records['tmdbContrarian'] = {
            'difference': round(avg_diff, 1),
            'type': 'generous' if avg_diff > 0 else 'harsh'
        }
    
    # Collection size milestones
    total = len(media_list)
    milestones = [10, 25, 50, 100, 250, 500, 1000]
    reached_milestone = max([m for m in milestones if m <= total], default=0)
    next_milestone = min([m for m in milestones if m > total], default=None)
    
    records['collectionMilestone'] = {
        'total': total,
        'reached': reached_milestone,
        'next': next_milestone,
        'progress': (total / next_milestone * 100) if next_milestone else 100
    }
    
    # Most productive genre (highest average rating)
    genre_ratings = {}
    for media in rated:
        if media.genres:
            genres = media.genres if isinstance(media.genres, list) else media.genres.split(', ')
            for genre in genres:
                if genre not in genre_ratings:
                    genre_ratings[genre] = []
                genre_ratings[genre].append(media.rating)
    
    # Only consider genres with at least 3 ratings
    qualified_genres = {g: ratings for g, ratings in genre_ratings.items() if len(ratings) >= 3}
    
    if qualified_genres:
        best_genre = max(qualified_genres.items(), key=lambda x: sum(x[1]) / len(x[1]))
        avg_rating = sum(best_genre[1]) / len(best_genre[1])
        records['bestGenre'] = {
            'genre': best_genre[0],
            'averageRating': round(avg_rating, 1),
            'count': len(best_genre[1])
        }
    
    return jsonify(records)


@analytics_bp.route('/collection-card', methods=['GET'])
@jwt_required()
def get_collection_card():
    """
    Get data for shareable collection card
    All-time stats, no time dependency
    """
    user_id = get_jwt_identity()
    
    media_list = Media.query.filter_by(user_id=user_id).all()
    watched = [m for m in media_list if m.status == 'watched']
    rated = [m for m in media_list if m.rating]
    
    # Basic stats
    stats = {
        'totalItems': len(media_list),
        'totalWatched': len(watched),
        'totalRated': len(rated)
    }
    
    # Average rating
    if rated:
        stats['averageRating'] = round(sum(m.rating for m in rated) / len(rated), 1)
    else:
        stats['averageRating'] = None
    
    # Top genre
    genre_counts = {}
    for media in media_list:
        if media.genres:
            genres = media.genres if isinstance(media.genres, list) else media.genres.split(', ')
            for genre in genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    if genre_counts:
        top_genre = max(genre_counts.items(), key=lambda x: x[1])
        stats['topGenre'] = top_genre[0]
        stats['topGenreCount'] = top_genre[1]
    
    # Favorite actor (top 1)
    actor_counts = {}
    for media in media_list:
        if media.cast:
            for cast_member in media.cast:
                actor_name = cast_member.get('name')
                if actor_name:
                    actor_counts[actor_name] = actor_counts.get(actor_name, 0) + 1
    
    if actor_counts:
        top_actor = max(actor_counts.items(), key=lambda x: x[1])
        stats['favoriteActor'] = top_actor[0]
        stats['favoriteActorCount'] = top_actor[1]
    
    # TMDB comparison
    media_with_both = [m for m in rated if m.tmdb_rating]
    if media_with_both:
        diffs = []
        for m in media_with_both:
            tmdb_5point = m.tmdb_rating / 2
            diff = m.rating - tmdb_5point
            diffs.append(diff)
        
        avg_diff = sum(diffs) / len(diffs)
        stats['tmdbDifference'] = round(avg_diff, 1)
    
    # Favorite decade
    decade_counts = {}
    for media in media_list:
        if media.release_year:
            decade = (media.release_year // 10) * 10
            decade_label = f"{decade}s"
            decade_counts[decade_label] = decade_counts.get(decade_label, 0) + 1
    
    if decade_counts:
        top_decade = max(decade_counts.items(), key=lambda x: x[1])
        stats['favoriteDecade'] = top_decade[0]
        stats['favoriteDecadeCount'] = top_decade[1]
    
    return jsonify(stats)