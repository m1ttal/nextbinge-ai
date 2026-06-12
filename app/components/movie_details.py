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
    """

    col1, col2 = st.columns(
        [1, 2]
    )

    with col1:

        poster_path = movie.get(
            "poster_path",
            ""
        )

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

        st.image(
            image_url,
            width = "stretch"
        )

    with col2:

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
            "Unknown"
        )

        runtime = movie.get(
            "runtime",
            None
        )

        language = movie.get(
            "language",
            "Unknown"
        )

        vote_count = movie.get(
            "vote_count",
            0
        )

        description = movie.get(
            "description",
            "No description available."
        )

        st.title(title)

        metric1, metric2, metric3 = (
            st.columns(3)
        )

        with metric1:
            st.metric(
                "⭐ Rating",
                f"{rating:.1f}"
            )

        with metric2:
            st.metric(
                "📅 Year",
                str(year)
            )

        with metric3:
            st.metric(
                "🗳 Votes",
                f"{int(vote_count):,}"
            )

        st.markdown(
            f"**Genres:** {genres}"
        )

        if runtime:
            st.markdown(
                f"**Runtime:** {int(runtime)} min"
            )

        st.markdown(
            f"**Language:** {language}"
        )

        st.markdown("### Overview")

        st.write(description)