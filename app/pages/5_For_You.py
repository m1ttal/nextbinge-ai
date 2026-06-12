import streamlit as st

from pathlib import Path
import sys
import random


# ==================================================
# Project Setup
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


from src.data.cache import (
    get_movie_master,
    get_item_genres
)

from src.recommenders.movies.popularity import (
    get_top_movies_by_genre,
    get_available_genres
)

from app.components.movie_cards import (
    render_movie_grid
)

from app.components.movie_details import (
    render_movie_details
)


# ==================================================
# Page Config
# ==================================================

st.set_page_config(
    page_title="For You | NextBinge AI",
    page_icon="💖",
    layout="wide"
)


# ==================================================
# Load Data
# ==================================================

movie_master = get_movie_master()

item_genres = get_item_genres()


# ==================================================
# Header
# ==================================================

st.title("💖 For You")

st.caption(
    "Discover movies based on mood, era, language, and pure curiosity."
)

st.divider()


# ==================================================
# Tabs
# ==================================================

discover_tab, era_tab, world_tab, surprise_tab = st.tabs(
    [
        "🎯 Discover",
        "📅 Explore Eras",
        "🌎 Explore Worlds",
        "🎲 Surprise Me"
    ]
)


# ==================================================
# DISCOVER
# ==================================================

with discover_tab:

    st.subheader(
        "🍿 Movie Night Generator"
    )

    quality_movies = movie_master[
        (movie_master["vote_average"] >= 7.0)
        &
        (movie_master["vote_count"] >= 500)
    ]

    if st.button(
        "🍿 Generate Tonight's Pick",
        key="movie_night",
        width="stretch"
    ):

        pick = (
            quality_movies
            .sample(1)
            .iloc[0]
        )

        render_movie_details(
            pick
        )

    st.divider()

    st.subheader(
        "😊 Mood Discovery"
    )

    mood_map = {

        "😀 Feel Good": [
            "Comedy",
            "Family"
        ],

        "💖 Romance": [
            "Romance"
        ],

        "🤯 Mind Bending": [
            "Science Fiction",
            "Mystery"
        ],

        "😱 Thriller Night": [
            "Thriller",
            "Horror"
        ],

        "⚔️ Action Packed": [
            "Action",
            "Adventure"
        ],

        "🧙 Fantasy Escape": [
            "Fantasy"
        ]
    }

    selected_mood = st.selectbox(
        "Choose Your Mood",
        list(mood_map.keys())
    )

    mood_genres = mood_map[
        selected_mood
    ]

    mood_item_ids = (
        item_genres[
            item_genres["genre"]
            .isin(mood_genres)
        ]["item_id"]
        .unique()
    )

    mood_movies = (
        movie_master[
            movie_master["item_id"]
            .isin(mood_item_ids)
        ]
        .sort_values(
            "vote_count",
            ascending=False
        )
        .head(10)
    )

    render_movie_grid(
        mood_movies,
        columns=5
    )


# ==================================================
# DECADE EXPLORER
# ==================================================

with era_tab:

    st.subheader(
        "📅 Decade Explorer"
    )

    decades = {
        "1980s": (1980, 1989),
        "1990s": (1990, 1999),
        "2000s": (2000, 2009),
        "2010s": (2010, 2019),
        "2020s": (2020, 2029)
    }

    selected_decade = st.selectbox(
        "Choose a Decade",
        list(decades.keys())
    )

    start_year, end_year = decades[
        selected_decade
    ]

    decade_movies = (
        movie_master[
            movie_master["release_year"]
            .between(
                start_year,
                end_year
            )
        ]
        .sort_values(
            "vote_count",
            ascending=False
        )
        .head(10)
    )

    render_movie_grid(
        decade_movies,
        columns=5
    )


# ==================================================
# LANGUAGE + GENRE
# ==================================================

with world_tab:

    st.subheader(
        "🎰 Genre Roulette"
    )

    genres = get_available_genres(
        item_genres
    )

    if st.button(
        "🎰 Spin Genre Roulette",
        key="genre_roulette",
        width="stretch"
    ):

        selected_genre = random.choice(
            genres
        )

        st.success(
            f"Selected Genre: {selected_genre}"
        )

        genre_movies = (
            get_top_movies_by_genre(
                movie_master=movie_master,
                item_genres=item_genres,
                genre=selected_genre,
                top_n=10
            )
        )

        render_movie_grid(
            genre_movies,
            columns=5
        )

    st.divider()

    st.subheader(
        "🌎 Language Explorer"
    )

    languages = sorted(
        movie_master["language"]
        .dropna()
        .unique()
    )

    selected_language = st.selectbox(
        "Choose Language",
        languages
    )

    language_movies = (
        movie_master[
            movie_master["language"]
            == selected_language
        ]
        .sort_values(
            "vote_count",
            ascending=False
        )
        .head(10)
    )

    render_movie_grid(
        language_movies,
        columns=5
    )

# ==================================================
# SURPRISE ME
# ==================================================

with surprise_tab:

    st.subheader(
        "🎲 Surprise Me"
    )

    if st.button(
        "🎲 Pick A Random Movie",
        key="random_movie",
        width="stretch"
    ):

        random_movie = (
            movie_master
            .sample(1)
            .iloc[0]
        )

        render_movie_details(
            random_movie
        )

    st.divider()

    st.subheader(
        "⏱️ Quick Watch"
    )

    quick_watch = (
        movie_master[
            (movie_master["runtime"] <= 90)
            &
            (movie_master["vote_average"] >= 6.5)
        ]
        .sort_values(
            "vote_count",
            ascending=False
        )
        .head(10)
    )

    render_movie_grid(
        quick_watch,
        columns=5
    )

st.divider()

# ==================================================
# Footer
# ==================================================

st.caption(
    "NextBinge AI • Personalized Discovery Experience"
)