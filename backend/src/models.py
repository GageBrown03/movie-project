from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import enum
from datetime import datetime

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


class FriendshipStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    BLOCKED = "blocked"


class ActivityType(enum.Enum):
    ADDED_MEDIA = "added_media"
    RATED_MEDIA = "rated_media"
    CHANGED_RATING = "changed_rating"
    MILESTONE = "milestone"
    JOINED = "joined"


class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # PHASE 2: NEW FIELDS
    username = db.Column(db.String(50), unique=True, nullable=True, index=True)
    display_name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    
    # Privacy settings (default: private)
    privacy_collection = db.Column(db.String(20), default='private')
    privacy_ratings = db.Column(db.String(20), default='private')
    privacy_stats = db.Column(db.String(20), default='private')
    privacy_profile_searchable = db.Column(db.Boolean, default=False)
    
    # Email notification preferences
    email_notifications_friend_requests = db.Column(db.Boolean, default=True)
    
    # Relationships
    media = db.relationship('Media', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # Friend relationships (using secondary table)
    friendships_initiated = db.relationship(
        'Friendship',
        foreign_keys='Friendship.user_id_1',
        backref='initiator',
        lazy='dynamic'
    )
    friendships_received = db.relationship(
        'Friendship',
        foreign_keys='Friendship.user_id_2',
        backref='receiver',
        lazy='dynamic'
    )
    
    # Activity feed
    activities = db.relationship('ActivityFeed', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, email, password, username=None):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.username = username
    
    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'userId': self.user_id,
            'email': self.email,
            'username': self.username,
            'displayName': self.display_name,
            'bio': self.bio,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'privacyCollection': self.privacy_collection,
            'privacyRatings': self.privacy_ratings,
            'privacyStats': self.privacy_stats,
            'privacyProfileSearchable': self.privacy_profile_searchable,
        }


class Friendship(db.Model):
    """
    Friendship table with normalized storage (user_id_1 < user_id_2)
    """
    __tablename__ = 'friendships'
    
    friendship_id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    status = db.Column(db.Enum(FriendshipStatus), default=FriendshipStatus.PENDING, nullable=False, index=True)
    requested_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    accepted_at = db.Column(db.DateTime, default=db.func.now())
    
    # Composite unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id_1', 'user_id_2', name='unique_friendship'),
        db.CheckConstraint('user_id_1 < user_id_2', name='ordered_friendship'),
        db.CheckConstraint('user_id_1 != user_id_2', name='no_self_friendship'),
    )
    
    def __init__(self, user_id_1, user_id_2, requested_by):
        # Ensure user_id_1 < user_id_2 (normalized storage)
        if user_id_1 > user_id_2:
            user_id_1, user_id_2 = user_id_2, user_id_1
        
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2
        self.requested_by = requested_by
    
    def to_dict(self, current_user_id):
        """
        Convert to dict from perspective of current_user_id
        """
        # Determine the other user
        other_user_id = self.user_id_2 if self.user_id_1 == current_user_id else self.user_id_1
        
        # Get other user's info
        other_user = User.query.get(other_user_id)
        
        # Determine request type
        request_type = 'sent' if self.requested_by == current_user_id else 'received'
        
        return {
            'friendshipId': self.friendship_id,
            'status': self.status.value,
            'requestType': request_type,
            'otherUserId': other_user_id,
            'otherUsername': other_user.username,
            'otherDisplayName': other_user.display_name,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'acceptedAt': self.accepted_at.isoformat() if self.accepted_at else None,
        }


class ActivityFeed(db.Model):
    """
    Activity feed for social features
    """
    __tablename__ = 'activity_feed'
    
    activity_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    activity_type = db.Column(db.Enum(ActivityType), nullable=False, index=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.media_id'), nullable=True)
    data = db.Column(db.JSON, nullable=True)  # Extra data as JSON
    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    
    # Relationship to media
    media = db.relationship('Media', backref='activities', lazy='joined')
    
    def __init__(self, user_id, activity_type, media_id=None, data=None):
        self.user_id = user_id
        self.activity_type = activity_type
        self.media_id = media_id
        self.data = data or {}
    
    def to_dict(self):
        result = {
            'activityId': self.activity_id,
            'userId': self.user_id,
            'activityType': self.activity_type.value,
            'mediaId': self.media_id,
            'data': self.data,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
        }
        
        # Include media info if available
        if self.media:
            result['media'] = {
                'title': self.media.title,
                'mediaType': self.media.media_type.value,
                'posterUrl': self.media.poster_url,
            }
        
        return result


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
    
    # TMDB data (cached from API)
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
            
            # TMDB data
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
        
        # Include cast if requested
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
    Join table linking Media to Actors with additional data.
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