"""
Actor utility functions for managing actor data from TMDB.

This module handles:
- Deduplicating actors across multiple media entries
- Creating/updating actor records in the database
- Associating actors with media via MediaCast join table
"""

from src.models import db, Actor, MediaCast


def get_or_create_actor(tmdb_id, name, profile_path=None):
    """
    Get existing actor by TMDB ID or create new one.
    
    Args:
        tmdb_id: TMDB actor ID (unique identifier)
        name: Actor's name
        profile_path: TMDB profile image path (optional)
    
    Returns:
        Actor: The existing or newly created Actor instance
    """
    # Check if actor already exists
    actor = Actor.query.filter_by(tmdb_id=tmdb_id).first()
    
    if actor:
        # Update profile URL if it changed (TMDB occasionally updates images)
        if profile_path and actor.profile_url != profile_path:
            actor.profile_url = profile_path
            db.session.commit()
        return actor
    
    # Create new actor
    new_actor = Actor(
        tmdb_id=tmdb_id,
        name=name,
        profile_url=profile_path
    )
    db.session.add(new_actor)
    db.session.commit()
    
    return new_actor


def add_cast_to_media(media_id, cast_data, max_actors=10):
    """
    Add cast members to a media entry.
    
    Args:
        media_id: ID of the media (movie or TV show)
        cast_data: List of cast dictionaries from TMDB API
                   Format: [{'id': 123, 'name': 'Actor Name', 
                            'character': 'Role', 'order': 0, 
                            'profile_path': '/path.jpg'}, ...]
        max_actors: Maximum number of actors to store (default: 10)
    
    Returns:
        int: Number of cast members added
    """
    # Remove existing cast for this media (in case of re-fetch)
    MediaCast.query.filter_by(media_id=media_id).delete()
    
    # Limit to top N actors
    cast_to_add = cast_data[:max_actors]
    
    added_count = 0
    for cast_member in cast_to_add:
        # Get or create actor
        tmdb_id = cast_member.get('id')
        name = cast_member.get('name')
        profile_path = cast_member.get('profile_path')
        
        if not tmdb_id or not name:
            continue  # Skip if missing critical data
        
        # Format profile URL
        profile_url = None
        if profile_path:
            profile_url = f"https://image.tmdb.org/t/p/w185{profile_path}"
        
        actor = get_or_create_actor(tmdb_id, name, profile_url)
        
        # Create MediaCast association
        media_cast = MediaCast(
            media_id=media_id,
            actor_id=actor.actor_id,
            character=cast_member.get('character'),
            order=cast_member.get('order', added_count)
        )
        db.session.add(media_cast)
        added_count += 1
    
    db.session.commit()
    return added_count


def get_media_cast(media_id, limit=5):
    """
    Get cast for a media entry, ordered by billing.
    
    Args:
        media_id: ID of the media
        limit: Maximum number of cast members to return (default: 5)
    
    Returns:
        list: List of dictionaries with actor info
              Format: [{'name': 'Actor', 'character': 'Role', 
                       'profileUrl': 'url', 'order': 0}, ...]
    """
    cast = MediaCast.query.filter_by(media_id=media_id).order_by(MediaCast.order).limit(limit).all()
    
    return [
        {
            'actorId': c.actor.actor_id,
            'name': c.actor.name,
            'character': c.character,
            'profileUrl': c.actor.profile_url,
            'order': c.order
        }
        for c in cast
    ]