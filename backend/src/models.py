from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class movie(db.Model):

    __tablename__ = 'movie'

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, title: str, director: str, rating: int) -> None:
        super().__init__()
        self.title = title
        self.director = director
        self.rating = rating

    def __repr__(self) -> str:
        return f'movie({self.title}, {self.director}, {self.rating})'
    
    def to_dict(self) -> dict[str: any]:
        return {
            'movieId': self.movie_id,
            'title': self.title,
            'director': self.director,
            'rating': self.rating,
        }