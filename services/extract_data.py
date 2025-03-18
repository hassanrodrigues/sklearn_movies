from concurrent.futures import ThreadPoolExecutor
import csv
from tqdm import tqdm
from typing import Dict
from services.transform_data import MovieData

def read_movies(filename: str) -> Dict[str, MovieData]:
    movies_dict = {}
    try:

        print(f"Lendo arquivo: {filename}")

        with open(filename, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            line_count = 0

            for row in tqdm(csv_reader, desc="Lendo filmes", unit="linha"):
                movie = MovieData(row["movieId"], row["title"], row["genres"])
                movies_dict[row["movieId"]] = movie
                line_count += 1

        return movies_dict
    except Exception as e:
        print(f"Erro ao ler filmes: {str(e)}")
        return {}


def read_tags(filename: str, movies_dict: Dict[str, MovieData]):
    try:

        with open(filename, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            line_count = 0

            for row in csv_reader:
                movie_id = row["movieId"]
                if movie_id in movies_dict:
                    movies_dict[movie_id].add_tag(row["tag"])
                line_count += 1
        print("Leitura de tags concluída.")
    except Exception as e:
        print(f"Erro ao ler tags: {str(e)}")


def read_ratings(filename: str, movies_dict: Dict[str, MovieData]):
    try:

        with open(filename, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            line_count = 0

            for row in csv_reader:
                movie_id = row["movieId"]
                if movie_id in movies_dict:
                    movies_dict[movie_id].add_rating(
                        float(row["rating"]), int(row["timestamp"])
                    )
                line_count += 1
        print("Leitura de avaliações concluída.")
    except Exception as e:
        print(f"Erro ao ler avaliações: {str(e)}")


def read_links(filename: str, movies_dict: Dict[str, MovieData]):
    try:

        with open(filename, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            line_count = 0

            for row in csv_reader:
                movie_id = row["movieId"]
                if movie_id in movies_dict:
                    movies_dict[movie_id].add_ratings_ids(
                        row.get("imdbId", ""), row.get("tmdbId", "")
                    )
                line_count += 1
        print("Leitura de links concluída.")
    except Exception as e:
        print(f"Erro ao ler links: {str(e)}")


def read_data_in_parallel(
    movies_file: str, tags_file: str, links_file: str, ratings_file: str
) -> Dict[str, MovieData]:
    movies_dict = read_movies(movies_file)

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(read_tags, tags_file, movies_dict),
            executor.submit(read_links, links_file, movies_dict),
            executor.submit(read_ratings, ratings_file, movies_dict),
        ]

        for future in futures:
            future.result()

    return movies_dict