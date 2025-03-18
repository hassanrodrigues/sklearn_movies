from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Movie(Base):
    __tablename__: str = "movies"

    movieId = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    genres = Column(String)
    tags = Column(String)
    imdbId = Column(String)
    tmdbId = Column(String)

    ratings = relationship("Rating", back_populates="movie")


class Rating(Base):
    __tablename__: str= "ratings"

    ratingId = Column(Integer, primary_key=True, autoincrement=True)
    movieId = Column(Integer, ForeignKey("movies.movieId"))
    rating = Column(Float)
    timestamp = Column(Integer)

    movie = relationship("Movie", back_populates="ratings")