from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import enum

db = SQLAlchemy()
bcrypt = Bcrypt()


# Enums for type safety
class MediaType(enum.Enum):
    MOVIE = "movie"
    TV = "tv"


class MediaStatus(enum.Enum):
    WANT_TO_WATCH = "want_to_watch"
    WATCHING = "watching"  # For TV shows in progress
    WATCHED = "watched"


class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # Relationship to media (movies + TV shows)
    media = db.relationship('Media', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'userId': self.user_id,
            'username': self.username,
            'email': self.email,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }


class Media(db.Model):
    __tablename__ = 'media'
    
    media_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # Type & Status
    media_type = db.Column(db.Enum(MediaType), nullable=False, index=True)
    status = db.Column(db.Enum(MediaStatus), default=MediaStatus.WATCHED, nullable=False, index=True)
    
    # Common fields (both movies & TV)
    title = db.Column(db.String(200), nullable=False)
    release_year = db.Column(db.Integer)
    plot = db.Column(db.Text)
    genres = db.Column(db.String(500))  # Comma-separated: "Action, Sci-Fi"
    
    # TMDB metadata (cached from API)
    tmdb_id = db.Column(db.Integer, index=True)  # Not unique - multiple users can add same media
    poster_url = db.Column(db.String(500))
    backdrop_url = db.Column(db.String(500))
    
    # External ratings
    imdb_rating = db.Column(db.Float)  # 0-10 scale
    tmdb_rating = db.Column(db.Float)  # 0-10 scale
    
    # User's personal data
    rating = db.Column(db.Integer)  # 1-5 stars, NULL if in watchlist (not rated yet)
    watched_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    
    # Movie-specific fields
    director = db.Column(db.String(200))
    runtime = db.Column(db.Integer)  # minutes
    
    # TV-specific fields
    number_of_seasons = db.Column(db.Integer)
    number_of_episodes = db.Column(db.Integer)
    show_status = db.Column(db.String(50))  # "Returning Series", "Ended", "Canceled"
    seasons_watched = db.Column(db.Integer)  # Optional: how many seasons user completed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # Relationships
    cast = db.relationship('MediaCast', back_populates='media', lazy='joined', cascade='all, delete-orphan')
    
    def __init__(self, title, media_type, user_id, status=MediaStatus.WATCHED, rating=None, **kwargs):
        """
        Required: title, media_type, user_id
        Optional: status, rating (if watched), director, runtime, plot, genres,
                  tmdb_id, poster_url, backdrop_url, imdb_rating, tmdb_rating,
                  watched_date, notes, number_of_seasons, number_of_episodes,
                  show_status, seasons_watched
        
        Note: If status=WATCHED, rating should be provided.
              If status=WANT_TO_WATCH, rating should be None.
        """
        self.title = title
        self.media_type = media_type
        self.user_id = user_id
        self.status = status
        self.rating = rating
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self, include_cast=False):
        """
        Convert to dictionary for API responses.
        
        Args:
            include_cast: If True, includes full cast list (expensive)
        """
        result = {
            'mediaId': self.media_id,
            'userId': self.user_id,
            
            # Type & Status
            'mediaType': self.media_type.value,
            'status': self.status.value,
            
            # Common fields
            'title': self.title,
            'releaseYear': self.release_year,
            'plot': self.plot,
            'genres': self.genres.split(',') if self.genres else [],
            
            # TMDB metadata
            'tmdbId': self.tmdb_id,
            'posterUrl': self.poster_url,
            'backdropUrl': self.backdrop_url,
            
            # External ratings
            'imdbRating': self.imdb_rating,
            'tmdbRating': self.tmdb_rating,
            
            # User's data
            'rating': self.rating,
            'watchedDate': self.watched_date.isoformat() if self.watched_date else None,
            'notes': self.notes,
            
            # Timestamps
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Add movie-specific fields
        if self.media_type == MediaType.MOVIE:
            result['director'] = self.director
            result['runtime'] = self.runtime
        
        # Add TV-specific fields
        elif self.media_type == MediaType.TV:
            result['numberOfSeasons'] = self.number_of_seasons
            result['numberOfEpisodes'] = self.number_of_episodes
            result['showStatus'] = self.show_status
            result['seasonsWatched'] = self.seasons_watched
        
        # Include cast if requested (top 5 by default for performance)
        if include_cast:
            cast_list = sorted(self.cast, key=lambda x: x.order if x.order is not None else 999)[:5]
            result['cast'] = [
                {
                    'actorId': c.actor.actor_id,
                    'name': c.actor.name,
                    'character': c.character,
                    'profileUrl': c.actor.profile_url,
                    'order': c.order
                }
                for c in cast_list
            ]
        
        return result


class Actor(db.Model):
    __tablename__ = 'actor'
    
    actor_id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, index=True, nullable=False)
    name = db.Column(db.String(200), nullable=False, index=True)
    profile_url = db.Column(db.String(500))  # TMDB profile image
    
    # Relationships
    media_appearances = db.relationship('MediaCast', back_populates='actor', lazy=True)
    
    def __init__(self, tmdb_id, name, profile_url=None):
        self.tmdb_id = tmdb_id
        self.name = name
        self.profile_url = profile_url
    
    def to_dict(self):
        return {
            'actorId': self.actor_id,
            'tmdbId': self.tmdb_id,
            'name': self.name,
            'profileUrl': self.profile_url
        }


class MediaCast(db.Model):
    """
    Join table linking Media to Actors with additional metadata.
    Stores which actors appeared in which media and their roles.
    """
    __tablename__ = 'media_cast'
    
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.media_id'), nullable=False, index=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.actor_id'), nullable=False, index=True)
    character = db.Column(db.String(200))  # Character name they played
    order = db.Column(db.Integer)  # Billing order (0 = top billing, 1 = second, etc.)
    
    # Relationships
    media = db.relationship('Media', back_populates='cast')
    actor = db.relationship('Actor', back_populates='media_appearances')
    
    def __init__(self, media_id, actor_id, character=None, order=None):
        self.media_id = media_id
        self.actor_id = actor_id
        self.character = character
        self.order = order