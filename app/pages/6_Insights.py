# app/pages/Insights.py

import streamlit as st
import plotly.express as px

from pathlib import Path
import sys


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


# ==================================================
# Page Config
# ==================================================

st.set_page_config(
    page_title="Insights | NextBinge AI",
    page_icon="📊",
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

st.title("📊 Insights")

st.caption(
    "Explore the dataset powering NextBinge AI."
)

st.divider()


# ==================================================
# Platform Scale
# ==================================================

st.header("🌍 Platform Scale")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Movies",
        f"{len(movie_master):,}"
    )

with col2:
    st.metric(
        "Genres",
        item_genres["genre"].nunique()
    )

with col3:
    st.metric(
        "Languages",
        movie_master["language"].nunique()
    )

with col4:
    st.metric(
        "Avg Rating",
        round(
            movie_master["vote_average"].mean(),
            2
        )
    )

st.divider()


# ==================================================
# Ratings Distribution
# ==================================================

st.header("⭐ Rating Distribution")

fig = px.histogram(
    movie_master,
    x="vote_average",
    nbins=20,
    title="Distribution of Movie Ratings"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()


# ==================================================
# Movies by Release Year
# ==================================================

st.header("📅 Movies By Release Year")

year_counts = (
    movie_master["release_year"]
    .dropna()
    .value_counts()
    .sort_index()
)

fig = px.line(
    x=year_counts.index,
    y=year_counts.values,
    labels={
        "x": "Release Year",
        "y": "Movies"
    },
    title="Movies Released Per Year"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()


# ==================================================
# Top Languages
# ==================================================

st.header("🌎 Top Languages")

language_counts = (
    movie_master["language"]
    .fillna("Unknown")
    .value_counts()
    .head(15)
)

fig = px.bar(
    x=language_counts.index,
    y=language_counts.values,
    labels={
        "x": "Language",
        "y": "Movies"
    },
    title="Top Languages"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()


# ==================================================
# Genre Distribution
# ==================================================

st.header("🎭 Genre Distribution")

genre_counts = (
    item_genres["genre"]
    .value_counts()
    .head(15)
)

fig = px.bar(
    x=genre_counts.values,
    y=genre_counts.index,
    orientation="h",
    labels={
        "x": "Movies",
        "y": "Genre"
    },
    title="Most Common Genres"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()


# ==================================================
# Runtime Analysis
# ==================================================

if "runtime" in movie_master.columns:

    st.header("⏱ Runtime Distribution")

    runtime_df = movie_master[
        movie_master["runtime"].notna()
    ]

    fig = px.histogram(
        runtime_df,
        x="runtime",
        nbins=30,
        title="Movie Runtime Distribution"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()


# ==================================================
# Top Rated Movies
# ==================================================

st.header("🏆 Highest Rated Movies")

top_rated = (
    movie_master[
        movie_master["vote_count"] >= 500
    ]
    .sort_values(
        "vote_average",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_rated[
        [
            "title",
            "release_year",
            "vote_average",
            "vote_count"
        ]
    ],
    width="stretch",
    hide_index=True
)

st.divider()


# ==================================================
# Most Popular Movies
# ==================================================

if "popularity" in movie_master.columns:

    st.header("🔥 Most Popular Movies")

    popular_movies = (
        movie_master
        .sort_values(
            "popularity",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        popular_movies[
            [
                "title",
                "release_year",
                "popularity",
                "vote_average"
            ]
        ],
        width="stretch",
        hide_index=True
    )

    st.divider()


# ==================================================
# Dataset Quality
# ==================================================

st.header("🧹 Dataset Quality")

quality1, quality2, quality3 = st.columns(3)

with quality1:

    st.metric(
        "Movies With Posters",
        f"{movie_master['poster_path'].notna().sum():,}"
    )

with quality2:

    st.metric(
        "Movies With Overview",
        f"{movie_master['description'].notna().sum():,}"
    )

with quality3:

    st.metric(
        "Movies With Runtime",
        f"{movie_master['runtime'].notna().sum():,}"
    )

st.divider()

# ==================================================
# Footer
# ==================================================

st.caption(
    "NextBinge AI • Dataset Analytics & Insights"
)