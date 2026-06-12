import pandas as pd


def calculate_weighted_rating(
    movies: pd.DataFrame,
    percentile: float = 0.90
) -> pd.DataFrame:
    """
    Calculate IMDb-style weighted rating.

    Parameters
    ----------
    movies : pd.DataFrame
        Movie dataframe.

    percentile : float, default=0.90
        Vote count threshold percentile.

    Returns
    -------
    pd.DataFrame
        Qualified movies with weighted_rating column.
    """

    if movies.empty:
        return movies.copy()

    required_columns = [
        "vote_average",
        "vote_count"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in movies.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    C = movies["vote_average"].mean()
    m = movies["vote_count"].quantile(percentile)

    qualified = movies[
        movies["vote_count"] >= m
    ].copy()

    qualified["weighted_rating"] = (
        (
            qualified["vote_count"]
            / (
                qualified["vote_count"]
                + m
            )
        )
        * qualified["vote_average"]
        +
        (
            m
            / (
                qualified["vote_count"]
                + m
            )
        )
        * C
    )

    return qualified


def get_trending_movies(
    movie_master: pd.DataFrame,
    top_n: int = 20
) -> pd.DataFrame:
    """
    Return trending movies based on popularity.
    """

    return (
        movie_master
        .sort_values(
            by="popularity",
            ascending=False
        )
        .head(top_n)
        .copy()
    )


def get_top_rated_movies(
    movie_master: pd.DataFrame,
    top_n: int = 20,
    percentile: float = 0.90
) -> pd.DataFrame:
    """
    Return IMDb-style top rated movies.
    """

    ranked = calculate_weighted_rating(
        movie_master,
        percentile
    )

    ranked = ranked.sort_values(
        by="weighted_rating",
        ascending=False
    )

    return ranked.head(top_n).copy()


def get_hidden_gems(
    movie_master: pd.DataFrame,
    min_rating: float = 7.5,
    min_votes: int = 50,
    max_votes: int = 500,
    min_runtime: int = 60,
    top_n: int = 20
) -> pd.DataFrame:
    """
    Return highly rated movies that have
    relatively low vote counts.

    Hidden Gems intentionally do NOT use
    weighted rating because the goal is to
    surface lesser-known movies.
    """

    gems = movie_master[
        (movie_master["vote_average"] >= min_rating)
        &
        (movie_master["vote_count"] >= min_votes)
        &
        (movie_master["vote_count"] <= max_votes)
        &
        (movie_master["runtime"] >= min_runtime)
    ].copy()

    gems = gems.sort_values(
        by=[
            "vote_average",
            "vote_count"
        ],
        ascending=[
            False,
            False
        ]
    )

    return gems.head(top_n)


def get_top_movies_by_genre(
    movie_master: pd.DataFrame,
    item_genres: pd.DataFrame,
    genre: str,
    top_n: int = 20,
    percentile: float = 0.90
) -> pd.DataFrame:
    """
    Return top rated movies for a genre
    using IMDb weighted rating.
    """

    genre_item_ids = item_genres.loc[
        item_genres["genre"].str.lower()
        == genre.lower(),
        "item_id"
    ].unique()

    genre_movies = movie_master[
        movie_master["item_id"].isin(
            genre_item_ids
        )
    ].copy()

    if genre_movies.empty:
        return genre_movies

    ranked = calculate_weighted_rating(
        genre_movies,
        percentile
    )

    ranked = ranked.sort_values(
        by="weighted_rating",
        ascending=False
    )

    return ranked.head(top_n)


def get_available_genres(
    item_genres: pd.DataFrame
) -> list[str]:
    """
    Return sorted list of available genres.
    """

    return sorted(
        item_genres["genre"]
        .dropna()
        .unique()
        .tolist()
    )