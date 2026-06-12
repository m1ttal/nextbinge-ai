import streamlit as st

from pathlib import Path
import sys
import base64


# ==================================================
# Project Setup
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


LOGO_PATH = (
    PROJECT_ROOT
    / "app"
    / "assets"
    / "logo_favicon.png"
)

# ==================================================
# Page Config
# ==================================================

st.set_page_config(
    page_title="About | NextBinge AI",
    page_icon="ℹ️",
    layout="wide"
)

# ==================================================
# Header
# ==================================================

st.title("ℹ️ About NextBinge AI")

st.caption(
    "Building the future of entertainment discovery."
)

st.divider()


# ==================================================
# Introduction
# ==================================================

with open(LOGO_PATH, "rb") as f:
    logo = base64.b64encode(f.read()).decode("utf-8")

st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
        <img src="data:image/png;base64,{logo}" width="42" style="vertical-align:middle;">
        <h2 style="margin:0; color:white;">What is NextBinge AI?</h2>
    </div>

    <p style="font-size:16px; color:#ccc; line-height:1.6; margin-top:4px;">
        <b>NextBinge AI</b> is your personal entertainment companion — helping you
        discover <b>movies</b>, <b>TV shows</b>, and <b>anime</b> without the endless scrolling.
    </p>

    <p style="font-size:15px; color:#aaa; line-height:1.6; margin-top:10px;">
        Powered by advanced <b>machine learning</b> and <b>recommendation algorithms</b>,
        it transforms browsing into a personalized journey — surfacing hidden gems,
        timeless classics, and the perfect binge for every mood.
    </p>

    <p style="font-size:15px; color:#aaa; line-height:1.6; margin-top:10px;">
        By blending <b>data engineering</b>, <b>AI‑driven insights</b>, and sleek interactive design,
        NextBinge AI creates a discovery experience that feels effortless,
        engaging, and uniquely crafted <b>for you</b>.
    </p>
""", unsafe_allow_html=True)

st.divider()

# ==================================================
# Mission
# ==================================================

st.header("🚀 Our Mission")

st.info(
    """
    Help users find their next favorite movie, TV show,
    or anime without endless scrolling.

    NextBinge AI focuses on intelligent discovery,
    personalization, and recommendation quality.
    """
)

st.divider()

# ==================================================
# Architecture
# ==================================================

st.header("🏗️ Platform Architecture")

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.subheader("📦 Data Layer")

        st.markdown(
            """
            - TMDB Datasets
            - Data Cleaning
            - Feature Engineering
            - Feature Store
            """
        )

with col2:

    with st.container(border=True):

        st.subheader("🧠 ML Layer")

        st.markdown(
            """
            - Popularity Models
            - Content Models
            - Similarity Search
            - Recommendation Logic
            """
        )

with col3:

    with st.container(border=True):

        st.subheader("🎨 Experience Layer")

        st.markdown(
            """
            - Streamlit UI
            - Discovery Pages
            - Search Experience
            - Recommendation Workflows
            """
        )

st.divider()


# ==================================================
# Recommendation Engines
# ==================================================

st.header("🧠 Recommendation Engines")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🔥 Popularity",
        "🎯 Content",
        "👥 Collaborative",
        "⚡ Hybrid"
    ]
)

with tab1:

    st.success("Implemented")

    st.markdown(
        """
        Recommends content using:

        - Ratings
        - Vote Counts
        - Popularity Signals
        - Weighted Ranking

        Examples:

        - Trending Movies
        - Top Rated Movies
        - Hidden Gems
        """
    )

with tab2:

    st.success("Implemented")

    st.markdown(
        """
        Uses metadata similarity to recommend content.

        Features include:

        - Genres
        - Keywords
        - Cast
        - Directors
        - Overview Text

        Powered by:

        - TF-IDF Vectorization
        - Cosine Similarity Search
        """
    )

with tab3:

    st.warning("Coming Soon")

    st.markdown(
        """
        Future implementation:

        - User Ratings
        - User Preferences
        - User Similarity
        - Matrix Factorization
        """
    )

with tab4:

    st.info("Planned")

    st.markdown(
        """
        Combine:

        - Popularity Signals
        - Content Similarity
        - Collaborative Filtering

        For highly personalized recommendations.
        """
    )

st.divider()


# ==================================================
# Entertainment Domains
# ==================================================

st.header("🎭 Entertainment Domains")

domain1, domain2, domain3 = st.columns(3)

with domain1:

    with st.container(border=True):

        st.subheader("🎬 Movies")

        st.success("Available")

        st.write(
            "Popularity and content-based recommendation engine."
        )

with domain2:

    with st.container(border=True):

        st.subheader("📺 TV Shows")

        st.warning("In Development")

        st.write(
            "Next entertainment domain being added."
        )

with domain3:

    with st.container(border=True):

        st.subheader("👾 Anime")

        st.info("Planned")

        st.write(
            "Future recommendation domain."
        )

st.divider()


# ==================================================
# Technology Stack
# ==================================================

st.header("⚙️ Technology Stack")

stack1, stack2, stack3, stack4 = st.columns(4)

with stack1:
    st.metric(
        "Backend",
        "Python"
    )

with stack2:
    st.metric(
        "Data",
        "Pandas"
    )

with stack3:
    st.metric(
        "ML",
        "Scikit-Learn"
    )

with stack4:
    st.metric(
        "Frontend",
        "Streamlit"
    )

st.divider()


# ==================================================
# Roadmap
# ==================================================

st.header("🗺️ Product Roadmap")

roadmap = {
    "Feature": [
        "Popularity-Based Recommender",
        "Content-Based Recommender",
        "Advanced Search",
        "TV Shows Domain",
        "Anime Domain",
        "Collaborative Filtering",
        "Hybrid Recommender",
        "User Profiles",
        "Personalized Recommendations"
    ],
    "Status": [
        "✅ Complete",
        "✅ Complete",
        "✅ Complete",
        "🚧 In Progress",
        "📅 Planned",
        "📅 Planned",
        "📅 Planned",
        "📅 Planned",
        "📅 Planned"
    ]
}

st.dataframe(
    roadmap,
    width="stretch",
    hide_index=True
)

st.divider()

# ==================================================
# Developer Journey
# ==================================================

st.header("👨‍💻 Developer Journey")

st.markdown(
    """
    NextBinge AI began as a movie recommendation system
    and is evolving into a complete multi-domain recommendation platform.

    The goal is not only to recommend content,
    but also to serve as a practical implementation
    of modern recommendation system concepts including:

    - Content-Based Filtering
    - Collaborative Filtering
    - Matrix Factorization
    - Hybrid Recommendation Systems
    - Personalization
    - Discovery Engines
    """
)

st.divider()

# ==================================================
# Footer
# ==================================================

st.caption(
    "NextBinge AI • Built with Python, Machine Learning, and a passion for entertainment discovery."
)