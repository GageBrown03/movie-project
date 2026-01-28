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
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # NEW: Link to user
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    watched_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    def __init__(self, title, director, rating, user_id, description=None, image_url=None):
        self.title = title
        self.director = director
        self.rating = rating
        self.user_id = user_id  # NEW: Store which user created this
        self.description = description
        self.image_url = image_url
    
    def to_dict(self):
        return {
            'movieId': self.movie_id,
            'userId': self.user_id,  # NEW: Include user_id in response
            'title': self.title,
            'director': self.director,
            'rating': self.rating,
            'description': self.description,
            'imageUrl': self.image_url,
            'watchedDate': self.watched_date.isoformat() if self.watched_date else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }