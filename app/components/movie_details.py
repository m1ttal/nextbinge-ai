import pandas as pd
import streamlit as st


TMDB_IMAGE_BASE_URL = (
    "https://image.tmdb.org/t/p/w500"
)

PLACEHOLDER_IMAGE = (
    "https://placehold.co/500x750?text=No+Poster"
)


def render_movie_details(
    movie: pd.Series
):
    """
    Render detailed movie information.
    Safely handles missing values.
    """

    # ==================================
    # Safe Value Extraction
    # ==================================

    title = (
        movie.get("display_title")
        or movie.get("title")
        or "Unknown Movie"
    )

    year = movie.get("release_year")

    rating = movie.get("vote_average")

    genres = movie.get(
        "genres",
        "Unknown"
    )

    runtime = movie.get("runtime")

    language = movie.get(
        "language",
        "Unknown"
    )

    vote_count = movie.get(
        "vote_count"
    )

    description = movie.get(
        "description",
        ""
    )

    poster_path = movie.get(
        "poster_path",
        ""
    )

    # ==================================
    # Formatting
    # ==================================

    year_text = (
        str(int(year))
        if pd.notna(year)
        else "N/A"
    )

    rating_text = (
        f"{float(rating):.1f}"
        if pd.notna(rating)
        else "N/A"
    )

    runtime_text = (
        f"{int(runtime)} min"
        if pd.notna(runtime)
        else "Not Available"
    )

    vote_count_text = (
        f"{int(vote_count):,}"
        if pd.notna(vote_count)
        else "N/A"
    )

    description_text = (
        description
        if pd.notna(description)
        and str(description).strip()
        else "No overview available."
    )

    language_text = (
        str(language).upper()
        if pd.notna(language)
        else "Unknown"
    )

    genres_text = (
        genres
        if pd.notna(genres)
        else "Unknown"
    )

    # ==================================
    # Poster
    # ==================================

    if (
        pd.notna(poster_path)
        and str(poster_path).strip()
    ):
        image_url = (
            TMDB_IMAGE_BASE_URL
            + str(poster_path)
        )
    else:
        image_url = (
            PLACEHOLDER_IMAGE
        )

    # ==================================
    # Layout
    # ==================================

    col1, col2 = st.columns(
        [1, 2]
    )

    with col1:

        st.image(
            image_url,
            width="stretch"
        )

    with col2:

        st.title(title)

        metric1, metric2, metric3 = (
            st.columns(3)
        )

        with metric1:
            st.metric(
                "⭐ Rating",
                rating_text
            )

        with metric2:
            st.metric(
                "📅 Year",
                year_text
            )

        with metric3:
            st.metric(
                "🗳 Votes",
                vote_count_text
            )

        st.markdown(
            f"**🎭 Genres:** {genres_text}"
        )

        st.markdown(
            f"**⏱ Runtime:** {runtime_text}"
        )

        st.markdown(
            f"**🌍 Language:** {language_text}"
        )

        st.markdown(
            "### 📖 Overview"
        )

        st.write(
            description_text
        )