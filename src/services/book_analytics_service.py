import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from src.domain.book import Book


class BookAnalyticsService:

    def average_price(self, books: list[Book]) -> float:
        prices = np.array([b.price_usd for b in books], dtype = float)
        return float(prices.mean())
    

    def top_rated(self, books: list[Book], min_ratings: int = 1000, limit: int = 10) -> list:
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count  for b in books])

        # filtered books: all books that have > 1000 ratings
        mask = counts > min_ratings
        filteredBooks = np.array(books)[mask]
        scores = ratings[mask]

        sorted_idx = np.argsort(scores)[::-1]

        return filteredBooks[sorted_idx].tolist()[:limit]

    def value_scores(self, books: list[Book]) -> dict[str, float]:
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count  for b in books])
        prices = np.array([b.ratings_count  for b in books])

        scores = (ratings * np.log1p(counts)) / prices
        return {
            book.book_id: float(score)
            for book, score in zip(books, scores)
        }
    
    # numpy version, replaced in repl usage by the pandas version
    def median_price_by_genre(self, books: list[Book]) -> dict[str, float]:

        prices_by_genre: dict[str, list[float]] = defaultdict(list)

        for b in books:
            if b.price_usd is not None and not np.isnan(b.price_usd):
                prices_by_genre[b.genre].append(float(b.price_usd))

        result: dict[str, float] = {}
        for genre, prices in prices_by_genre.items():
            if len(prices) == 0:
                continue
            result[genre] = float(np.median(np.array(prices)))

        return result


    def price_std_dev(self, books: list[Book]) -> tuple[float, float]:
        prices = np.array(
            [b.price_usd for b in books if b.price_usd is not None and not np.isnan(b.price_usd)],
            dtype=float
        )

        if prices.size == 0:
            return (float("nan"), float("nan"))

        pop_std = float(prices.std(ddof=0))
        sample_std = float(prices.std(ddof=1)) if prices.size >= 2 else float("nan")

        return pop_std, sample_std


    def price_percentiles(self, books: list[Book], percentiles: list[float]) -> list[float]:
        for p in percentiles:
            if p < 0 or p > 100:
                raise ValueError(f"Percentile {p} out of bounds [0, 100]")

        prices = np.array(
            [b.price_usd for b in books if b.price_usd is not None and not np.isnan(b.price_usd)],
            dtype=float
        )

        if prices.size == 0:
            return [float("nan")] * len(percentiles)

        values = np.percentile(prices, percentiles)
        return [float(v) for v in values]

    def rating_price_correlation(self, books: list[Book]) -> float:
        ratings = []
        prices = []

        for b in books:
            if (
                b.average_rating is not None
                and b.price_usd is not None
                and not np.isnan(b.average_rating)
                and not np.isnan(b.price_usd)
            ):
                ratings.append(b.average_rating)
                prices.append(b.price_usd)

        if len(ratings) < 2:
            return float("nan")

        ratings_arr = np.array(ratings, dtype=float)
        prices_arr = np.array(prices, dtype=float)

        if np.std(ratings_arr) == 0 or np.std(prices_arr) == 0:
            return float("nan")

        corr = np.corrcoef(ratings_arr, prices_arr)[0, 1]
        return float(corr)


    def rating_histogram(self, books: list[Book], bins: int = 10) -> tuple[list[int], list[float]]:

        ratings = np.array(
            [b.average_rating for b in books if b.average_rating is not None and not np.isnan(b.average_rating)],
            dtype=float
        )

        if ratings.size == 0:
            return [], []

        counts, bin_edges = np.histogram(ratings, bins=bins)

        return counts.tolist(), bin_edges.tolist()

    def most_popular_genre_2026(self, books: list[Book]) -> int:
        # get the most popular genre in 2026 in by count of checkouts in 2026
        genre_counts = {}

        for book in books:
            if book.genre is None or book.last_checkout is None:
                continue

            try:
                checkout_year = datetime.fromisoformat(book.last_checkout).year
            except ValueError:
                continue

            if checkout_year == 2026: 
                if book.genre in genre_counts:
                    genre_counts[book.genre] += 1
                else:
                    genre_counts[book.genre] = 1

        # Return the genre with the highest number of checkouts
        return max(genre_counts, key=genre_counts.get)

    def _books_to_df(self, books: list[Book]) -> pd.DataFrame:
        df = pd.DataFrame([b.to_dict() for b in books])

        # ---- Clean data ----
        df = df.dropna(subset=["genre", "average_rating", "ratings_count"])
        df = df[df["ratings_count"] > 0]
        df = df[df["price_usd"] > 0]
        df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")

        return df

    def plot_most_common_genres(self, books: list[Book]) -> None:
        df = self._books_to_df(books)

        genre_counts = df["genre"].value_counts()

        genre_counts.plot(kind="bar", title="Most Common Book Genres")
        plt.xlabel("Genre")
        plt.ylabel("Number of Books")
        plt.tight_layout()
        plt.show()

    def plot_highest_rated_genres(self, books: list[Book], m: int = 75) -> None:
        df = self._books_to_df(books)

        global_average = df["average_rating"].mean()

        genre_stats = (
            df.groupby("genre")
            .agg(
                average_rating=("average_rating", "mean"),
                ratings_count=("ratings_count", "sum")
            )
        )

        genre_stats["weighted_rating"] = (
            (genre_stats["ratings_count"] /
            (genre_stats["ratings_count"] + m)) * genre_stats["average_rating"]
            + (m / (genre_stats["ratings_count"] + m)) * global_average
        )

        genre_stats.sort_values("weighted_rating", ascending=False)["weighted_rating"] \
            .plot(kind="bar", title="Highest Rated Genres (Bayesian Average)")

        plt.xlabel("Genre")
        plt.ylabel("Weighted Rating")
        plt.tight_layout()
        plt.show()

    def plot_price_vs_rating(self, books: list[Book]) -> None:
        df = self._books_to_df(books)

        plt.scatter(df["price_usd"], df["average_rating"], alpha=0.6)
        plt.title("Book Price vs Average Rating")
        plt.xlabel("Price (USD)")
        plt.ylabel("Average Rating")
        plt.tight_layout()
        plt.show()

    def plot_books_by_year(self, books: list[Book]) -> None:
        df = self._books_to_df(books)

        yearly_counts = (
            df.dropna(subset=["release_year"])
            .groupby("release_year")
            .size()
        )

        yearly_counts.plot(kind="line", title="Books Released by Year")
        plt.xlabel("Year")
        plt.ylabel("Number of Books")
        plt.tight_layout()
        plt.show()

    def plot_checked_out_vs_available(self, books: list[Book]) -> None:
        df = self._books_to_df(books)

        status_counts = df["available"].value_counts()
        status_counts = status_counts.rename({
            True: "Available",
            False: "Checked Out"
        })

        status_counts.plot(kind="pie", autopct="%1.1f%%", title="Book Availability")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()
