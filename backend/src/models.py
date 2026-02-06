from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # Relationship to movies
    movies = db.relationship('Movie', backref='user', lazy=True, cascade='all, delete-orphan')
    
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


class Movie(db.Model):
    __tablename__ = 'movie'
    
    movie_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # Basic info (user can override these)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(200))
    release_year = db.Column(db.Integer)
    runtime = db.Column(db.Integer)  # minutes
    plot = db.Column(db.Text)
    genres = db.Column(db.String(500))  # Comma-separated for now, e.g. "Action, Sci-Fi"
    
    # TMDB metadata (cached from API)
    tmdb_id = db.Column(db.Integer, unique=False, index=True)  # Not unique - multiple users can add same movie
    poster_url = db.Column(db.String(500))
    backdrop_url = db.Column(db.String(500))
    
    # External ratings (fetched from TMDB, which aggregates them)
    imdb_rating = db.Column(db.Float)  # 0-10 scale
    tmdb_rating = db.Column(db.Float)  # 0-10 scale
    
    # User's personal data
    rating = db.Column(db.Integer, nullable=False)  # User's 1-5 rating
    watched_date = db.Column(db.Date)
    notes = db.Column(db.Text)  # Personal notes (future: rename from description)
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    def __init__(self, title, rating, user_id, **kwargs):
        """
        Required: title, rating, user_id
        Optional: director, release_year, runtime, plot, genres, 
                  tmdb_id, poster_url, backdrop_url, 
                  imdb_rating, tmdb_rating, watched_date, notes
        """
        self.title = title
        self.rating = rating
        self.user_id = user_id
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        return {
            'movieId': self.movie_id,
            'userId': self.user_id,
            
            # Basic info
            'title': self.title,
            'director': self.director,
            'releaseYear': self.release_year,
            'runtime': self.runtime,
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
            
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }