import streamlit as st
from streamlit_searchbox import st_searchbox

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


from src.data.cache import (
    get_movie_master,
    get_item_genres,
    get_movie_content_artifacts
)

from src.recommenders.movies.content import (
    search_movie,
    get_movie_by_display_title,
    get_similar_movies
)

from src.recommenders.movies.popularity import (
    get_trending_movies,
    get_top_rated_movies,
    get_hidden_gems,
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
# Page Configuration
# ==================================================

st.set_page_config(
    page_title="Movies | NextBinge AI",
    page_icon="🎬",
    layout="wide"
)


# ==================================================
# Load Data
# ==================================================

movie_master = get_movie_master()

item_genres = get_item_genres()

tfidf_matrix, item_lookup = (
    get_movie_content_artifacts()
)


# ==================================================
# Search Callback
# ==================================================

def search_titles(searchterm: str):

    if not searchterm:
        return []

    matches = search_movie(
        query=searchterm,
        movie_master=movie_master,
        limit=10
    )

    if matches.empty:
        return []

    return matches["display_title"].tolist()


# ==================================================
# Header
# ==================================================

st.title("🎬 Movies")

st.caption(
    "Discover movies, explore trends, and get AI-powered recommendations."
)


# ==================================================
# Search & Recommendations
# ==================================================

with st.container(border=True):

    st.header(
        "🔍 Find Your Next Binge"
    )

    st.caption(
        "Search for a movie and get personalized recommendations."
    )

    selected_movie_display = (
        st_searchbox(
            search_function=search_titles,
            placeholder="Search movies..."
        )
    )


# ==================================================
# Movie Details + Similar Movies
# ==================================================

if selected_movie_display:

    try:

        selected_movie = (
            get_movie_by_display_title(
                selected_movie_display,
                movie_master
            )
        )

        st.divider()

        render_movie_details(
            selected_movie
        )

        st.divider()

        recommendations = (
            get_similar_movies(
                item_id=int(
                    selected_movie["item_id"]
                ),
                movie_master=movie_master,
                tfidf_matrix=tfidf_matrix,
                item_lookup=item_lookup,
                top_n=10
            )
        )

        st.subheader(
            f"🎯 Because You Liked {selected_movie['title']}"
        )

        render_movie_grid(
            recommendations,
            columns=5
        )

        st.divider()

    except Exception as e:

        st.error(
            f"Recommendation error: {e}"
        )


# ==================================================
# Discovery Hub
# ==================================================

st.header(
    "🎥 Discover Movies"
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🔥 Trending",
        "⭐ Top Rated",
        "💎 Hidden Gems",
        "🎭 Genres"
    ]
)

with tab1:

    trending_movies = (
        get_trending_movies(
            movie_master,
            top_n=15
        )
    )

    render_movie_grid(
        trending_movies,
        columns=5
    )

with tab2:

    top_rated_movies = (
        get_top_rated_movies(
            movie_master,
            top_n=15
        )
    )

    render_movie_grid(
        top_rated_movies,
        columns=5
    )

with tab3:

    hidden_gems = (
        get_hidden_gems(
            movie_master,
            top_n=15
        )
    )

    render_movie_grid(
        hidden_gems,
        columns=5
    )

with tab4:

    genres = get_available_genres(
        item_genres
    )

    selected_genre = st.selectbox(
        "Select Genre",
        genres
    )

    genre_movies = (
        get_top_movies_by_genre(
            movie_master=movie_master,
            item_genres=item_genres,
            genre=selected_genre,
            top_n=15
        )
    )

    render_movie_grid(
        genre_movies,
        columns=5
    )

st.divider()

# ==================================================
# Footer
# ==================================================

st.caption(
    "NextBinge AI • Movie Discovery & Recommendation Engine"
)