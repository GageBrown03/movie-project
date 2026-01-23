from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movie'

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, title, director, rating):
        self.title = title
        self.director = director
        self.rating = rating

    def to_dict(self):
        return {
            'movieId': self.movie_id,
            'title': self.title,
            'director': self.director,
            'rating': self.rating
        }