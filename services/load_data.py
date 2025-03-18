from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.models import Movie, Rating
from typing import List
from services.transform_data import MovieData
import sys

DATABASE_URL = "sqlite:///movies.db"
engine = create_engine(DATABASE_URL, echo=False)

def get_db():
    return Session(engine)

def save_to_sqlalchemy(movies: List[MovieData]):
    db: Session = get_db()

    try:
        print("Excluindo filmes e avaliações existentes...")
        db.query(Rating).delete()
        db.query(Movie).delete()
        db.commit()

        total_movies = len(movies)
        total_ratings = sum(len(movie.ratings) for movie in movies)
        inserted_movies = 0
        inserted_ratings = 0

        movies_to_insert = []
        ratings_to_insert = []

        print(f"Total de filmes a serem inseridos: {total_movies}")
        print(f"Total de avaliações a serem inseridas: {total_ratings}")

        for movie in movies:
            db_movie = Movie(
                movieId=int(movie.movieId),
                title=movie.title,
                year=int(movie.year) if movie.year else None,
                genres="|".join(movie.genres),
                tags="|".join(movie.tags),
                imdbId=movie.imdbId,
                tmdbId=movie.tmdbId,
            )
            movies_to_insert.append(db_movie)
            inserted_movies += 1

            for rating in movie.ratings:
                db_rating = Rating(
                    movieId=int(movie.movieId),
                    rating=rating["rating"],
                    timestamp=rating["timestamp"],
                )
                ratings_to_insert.append(db_rating)
                inserted_ratings += 1

            if len(movies_to_insert) >= 50:
                print(f"Inserindo lote de filmes e avaliações...")
                db.bulk_save_objects(movies_to_insert)
                db.bulk_save_objects(ratings_to_insert)
                db.commit()

                movies_to_insert = []
                ratings_to_insert = []

            movie_progress = (
                (inserted_movies / total_movies) * 100 if total_movies else 0
            )
            rating_progress = (
                (inserted_ratings / total_ratings) * 100 if total_ratings else 0
            )

            sys.stdout.write(
                f"\rProgresso: Filmes {movie_progress:.2f}% | Avaliações {rating_progress:.2f}% "
            )
            sys.stdout.flush()

        if movies_to_insert:
            print(f"Inserindo último lote de filmes...")
            db.bulk_save_objects(movies_to_insert)
        if ratings_to_insert:
            print(f"Inserindo último lote de avaliações...")
            db.bulk_save_objects(ratings_to_insert)
        db.commit()

        print("\nDados salvos com sucesso no banco de dados SQLite!")

    except SQLAlchemyError as e:
        db.rollback()
        print(f"\nErro ao salvar no banco de dados: {str(e)}")
    finally:
        db.close()
from models.models import Base
Base.metadata.create_all(engine)