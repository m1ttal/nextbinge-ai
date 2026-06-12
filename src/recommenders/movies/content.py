import pandas as pd

from rapidfuzz import (
    fuzz,
    process
)

from sklearn.metrics.pairwise import (
    linear_kernel
)


def get_movie_by_display_title(
    display_title: str,
    movie_master: pd.DataFrame
) -> pd.Series:
    """
    Return movie by unique display title.

    Example:
    Interstellar (2014)
    """

    match = movie_master[
        movie_master["display_title"]
        == display_title
    ]

    if match.empty:

        raise ValueError(
            f"Movie '{display_title}' not found."
        )

    return match.iloc[0]


def search_movie(
    query: str,
    movie_master: pd.DataFrame,
    limit: int = 10
) -> pd.DataFrame:
    """
    Hybrid movie search.

    Ranking:
    1. Exact match
    2. Starts with
    3. Contains
    4. Fuzzy fallback
    """

    if not query:
        return pd.DataFrame()

    query = (
        query
        .strip()
        .lower()
    )

    # ==================================
    # Exact Match
    # ==================================

    exact = movie_master[
        movie_master["search_text"]
        == query
    ].copy()

    exact["match_type"] = 0

    # ==================================
    # Starts With
    # ==================================

    starts_with = movie_master[
        movie_master["search_text"]
        .str.startswith(
            query,
            na=False
        )
    ].copy()

    starts_with["match_type"] = 1

    # ==================================
    # Contains
    # ==================================

    contains = movie_master[
        movie_master["search_text"]
        .str.contains(
            query,
            na=False
        )
    ].copy()

    contains["match_type"] = 2

    # ==================================
    # Combine Strong Matches
    # ==================================

    combined = pd.concat(
        [
            exact,
            starts_with,
            contains
        ]
    )

    combined = (
        combined
        .drop_duplicates(
            subset="item_id"
        )
    )

    # ==================================
    # Return Strong Matches
    # ==================================

    if not combined.empty:

        return (
            combined
            .sort_values(
                [
                    "match_type",
                    "vote_count"
                ],
                ascending=[
                    True,
                    False
                ]
            )
            .head(limit)
            .reset_index(
                drop=True
            )
        )

    # ==================================
    # Fuzzy Fallback
    # ==================================

    matches = process.extract(
        query,
        movie_master[
            "search_text"
        ].tolist(),
        scorer=fuzz.token_set_ratio,
        limit=limit,
        score_cutoff=75
    )

    if not matches:
        return pd.DataFrame()

    fuzzy_titles = [
        match[0]
        for match in matches
    ]

    fuzzy_df = movie_master[
        movie_master[
            "search_text"
        ].isin(
            fuzzy_titles
        )
    ].copy()

    fuzzy_df["match_type"] = 3

    return (
        fuzzy_df
        .sort_values(
            "vote_count",
            ascending=False
        )
        .head(limit)
        .reset_index(
            drop=True
        )
    )


def get_similar_movies(
    item_id: int,
    movie_master: pd.DataFrame,
    tfidf_matrix,
    item_lookup,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Generate content-based recommendations.
    """

    if item_id not in item_lookup:

        raise ValueError(
            f"Item ID {item_id} not found."
        )

    idx = item_lookup[item_id]

    similarity_scores = (
        linear_kernel(
            tfidf_matrix[idx],
            tfidf_matrix
        )
        .flatten()
    )

    similar_indices = (
        similarity_scores
        .argsort()[::-1]
    )

    similar_indices = [
        i
        for i in similar_indices
        if i != idx
    ]

    top_indices = (
        similar_indices[:top_n]
    )

    recommendations = (
        movie_master
        .iloc[top_indices]
        [
            [
                "item_id",
                "display_title",
                "title",
                "poster_path",
                "vote_average",
                "vote_count",
                "release_year",
                "genres"
            ]
        ]
        .copy()
    )

    recommendations[
        "similarity_score"
    ] = (
        similarity_scores[
            top_indices
        ]
        .round(4)
    )

    return (
        recommendations
        .reset_index(
            drop=True
        )
    )