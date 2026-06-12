import streamlit as st
import pandas as pd


TMDB_IMAGE_BASE_URL = (
    "https://image.tmdb.org/t/p/w500"
)

PLACEHOLDER_IMAGE = (
    "https://placehold.co/500x750?text=No+Poster"
)


def render_movie_card(
    movie: pd.Series
):
    """
    Render a movie card.
    """

    poster_path = movie.get(
        "poster_path",
        ""
    )

    title = movie.get(
        "title",
        "Unknown"
    )

    year = movie.get(
        "release_year",
        "N/A"
    )

    rating = movie.get(
        "vote_average",
        0
    )

    genres = movie.get(
        "genres",
        ""
    )

    similarity_score = movie.get(
        "similarity_score",
        None
    )

    # -------------------------
    # Poster
    # -------------------------

    if (
        pd.notna(poster_path)
        and str(poster_path).strip()
    ):
        image_url = (
            TMDB_IMAGE_BASE_URL
            + str(poster_path)
        )
    else:
        image_url = PLACEHOLDER_IMAGE

    st.image(
        image_url,
        width = "stretch"
    )

    # -------------------------
    # Clean values
    # -------------------------

    if pd.isna(year):
        year = "N/A"

    if pd.isna(rating):
        rating = 0

    # -------------------------
    # Genres
    # -------------------------

    if (
        pd.notna(genres)
        and str(genres).strip()
    ):
        genre_text = (
            str(genres)
            .split("|")[:3]
        )

        genre_text = (
            " | ".join(genre_text)
        )
    else:
        genre_text = "Unknown"

    # -------------------------
    # Display
    # -------------------------

    st.markdown(
        f"**{title}**"
    )

    st.caption(
        f"📅 {year}"
    )

    st.caption(
        f"⭐ {rating:.1f}"
    )

    st.caption(
        f"🎭 {genre_text}"
    )

    # -------------------------
    # Similarity Score
    # -------------------------

    if similarity_score is not None:

        st.caption(
            f"🎯 Match: "
            f"{similarity_score:.2f}"
        )


def render_movie_grid(
    movies: pd.DataFrame,
    columns: int = 5
):
    """
    Render movies in a grid layout.
    """

    if movies.empty:

        st.info(
            "No movies found."
        )

        return

    for start in range(
        0,
        len(movies),
        columns
    ):

        cols = st.columns(
            columns
        )

        for idx, col in enumerate(cols):

            movie_idx = (
                start + idx
            )

            if movie_idx >= len(movies):
                continue

            with col:

                render_movie_card(
                    movies.iloc[
                        movie_idx
                    ]
                )