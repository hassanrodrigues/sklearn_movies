from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
import sqlite3
from models.models import Movie

def fetch_all_movies(db_path: str) -> List[Movie]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT movieId, title, genres, tags FROM movies")
    rows = cursor.fetchall()
    conn.close()

    return [Movie(movieId=row[0], title=row[1], genres=row[2], tags=row[3]) for row in rows]


def get_movie_index_by_title(movies: List[Movie], title: str):
    return next((i for i, m in enumerate(movies) if m.title.lower() == title.lower()), None)


def compute_similarity_matrix(movies: List[Movie]):
    tfidf = TfidfVectorizer(stop_words="english")

    movie_features = [f"{m.genres} {m.tags}" for m in movies]
    return cosine_similarity(tfidf.fit_transform(movie_features))


def recommend_movies_func_by_titles(movie_titles: List[str], db_path: str) -> List[Movie]:
    movies = fetch_all_movies(db_path)
    if not movies:
        return []

    cosine_sim = compute_similarity_matrix(movies)
    recommended_indices = set()

    for title in movie_titles:
        idx = get_movie_index_by_title(movies, title)
        if idx is not None:
            similar_movies = sorted(
                enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True
            )[1:11]
            recommended_indices.update(i for i, _ in similar_movies)
        else:
            print(f"Filme '{title}' não encontrado na lista.")

    return [movies[i] for i in recommended_indices][:10]


if __name__ == "__main__":
    DB_PATH = "movies.db"

    movie_titles = ["Toy Story", "Jumanji"]
    recommended = recommend_movies_func_by_titles(movie_titles, DB_PATH)

    print("Filmes recomendados:")
    for movie in recommended:
        print(f"ID: {movie.movieId}, Título: {movie.title}, Gêneros: {movie.genres}, Tags: {movie.tags}")