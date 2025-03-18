import re


class MovieData:
    def __init__(self, movieId, title, genres):
        self.movieId = movieId
        year_match = re.search(r"\((\d{4})\)", title)
        self.year = year_match.group(1) if year_match else None
        self.title = re.sub(r"\s*\(\d{4}\)", "", title).strip() if year_match else title
        self.genres = genres.split("|") if genres else []
        self.tags = []
        self.imdbId = ""
        self.tmdbId = ""
        self.ratings = []

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)

    def add_ratings_ids(self, imdbId: str, tmdbId: str):
        self.imdbId = imdbId
        self.tmdbId = tmdbId

    def add_rating(self, rating: float, timestamp: int):
        self.ratings.append({"rating": rating, "timestamp": timestamp})