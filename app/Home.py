import streamlit as st

from pathlib import Path
import sys
import base64

# ==================================================
# Project Setup
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))



LOGO_PATH = (
    PROJECT_ROOT
    / "app"
    / "assets"
    / "logo_favicon.png"
)

HERO_PATH = (
    PROJECT_ROOT
    / "app"
    / "assets"
    / "logo_hero.png"
)


# ==================================================
# Page Configuration
# ==================================================

st.set_page_config(
    page_title="NextBinge AI",
    page_icon=str(LOGO_PATH),
    layout="wide"
)


# Open the file using your Path object
with open(LOGO_PATH, "rb") as f:
    logo = base64.b64encode(f.read()).decode("utf-8")

st.markdown(f"""
    <style>
    [data-testid="stSidebar"]::before {{
        content: "";
        display: block;
        background-image: url("data:image/png;base64,{logo}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        height: 70px;
        margin-top: 50px;
        margin-bottom: 0px;

    }}
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #0E1117;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }

    /* Navigation items */
    [data-testid="stSidebarNav"] ul {
        list-style-type: none;
        padding-left: 0;
        margin-top: 0 !important;
    }

    [data-testid="stSidebarNav"] li a {
        color: #ccc !important;
        font-size: 16px;
        padding: 10px 15px;
        display: block;
        border-radius: 8px;
        transition: 0.3s;
    }

    /* Hover effect */
    [data-testid="stSidebarNav"] li a:hover {
        color: #fff !important;
        background: linear-gradient(90deg, #6a00f4, #00aaff);
        text-decoration: none;
    }

    /* Active page highlight */
    [data-testid="stSidebarNav"] li a.active {
        color: #fff !important;
        background: linear-gradient(90deg, #6a00f4, #00aaff);
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


# ==================================================
# Hero Section
# ==================================================

st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem;   /* remove top padding */
    }
    </style>
""", unsafe_allow_html=True)


st.markdown(f"""
    <div style="overflow:hidden; white-space:nowrap; background:#0E1117; padding:12px; border-radius:6px;">
        <marquee scrollamount="12" style="font-size:22px; font-weight:bold; color:#00aaff;">
            <img src="data:image/png;base64,{logo}" width="24" style="vertical-align:middle; margin-right:8px;">
            Your Next Favorite Awaits · Smart AI Recommendations · Movies 🎬 · TV Shows 📺 · Anime 👾 · Hidden Gems 💎 · Personalized Just For You ⭐
        </marquee>
    </div>
""", unsafe_allow_html=True)



left, center, right = st.columns([0.05, 10, 0.05])

with center:
    st.image(
        str(HERO_PATH),
        width="stretch"
    )

st.divider()

# ==================================================
# Quick Access
# ==================================================

st.header("🚀 Quick Access")

# Custom CSS to make the container feel like a clickable card
st.markdown("""
    <style>
    /* Targeting the column container to look like a card */
    [data-testid="stVerticalBlockBorderWrapper"] {
        transition: 0.3s;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 0 15px rgba(0, 150, 255, 0.6);
        border-color: #00aaff !important;
    }
    </style>
""", unsafe_allow_html=True)

def create_nav_card(label, page_path, icon, description):
    # Use border=True to create the box natively
    with st.container(border=True):
        # We use st.page_link as the primary navigation tool
        # label="" keeps it clean, we put the content inside columns or directly
        st.markdown(f"<h3 style='text-align: center; color: #00aaff;'>{icon} {label}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 14px;'>{description}</p>", unsafe_allow_html=True)
        
        # Center the link button
        col_dummy, col_btn, col_dummy2 = st.columns([1, 1, 1])
        with col_btn:
            st.page_link(page_path, label="View Section", icon="👉")

# Usage
cols = st.columns(3)

# Ensure the paths point to the correct files in your 'pages' directory
with cols[0]:
    create_nav_card("Movies", "pages/2_Movies.py", "🎬", "Search movies, explore genres, and discover recommendations.")
with cols[1]:
    create_nav_card("TV Shows", "pages/3_TV_Shows.py", "📺", "TV Show recommendation engine under development.")
with cols[2]:
    create_nav_card("Anime", "pages/4_Anime.py", "👾", "Anime recommendation engine planned for future releases.")

st.divider()


# ==================================================
# Why NextBinge AI?
# ==================================================

st.header("✨ Why NextBinge AI?")

c1, c2, c3 = st.columns(3)

with c1:

    with st.container(border=True):

        st.subheader(
            "🔍 Smart Discovery"
        )

        st.write(
            """
            Discover content through intelligent search,
            genre exploration, and recommendation engines.
            """
        )

with c2:

    with st.container(border=True):

        st.subheader(
            "🎯 Your Perfect Match"
        )

        st.write(
            """
            Receive recommendations based on content similarity,
            metadata, genres, cast, and storyline features.
            """
        )

with c3:

    with st.container(border=True):

        st.subheader(
            "🌐 NextBinge Smart Hub"
        )

        st.write(
            """
            Built to support Movies, TV Shows, Anime,
            and future entertainment domains.
            """
        )

st.divider()


# ==================================================
# Entertainment Domains
# ==================================================

st.header("🎭 Entertainment Domains")

tab1, tab2, tab3 = st.tabs(
    [
        "🎬 Movies",
        "📺 TV Shows",
        "👾 Anime"
    ]
)

with tab1:

    st.success(
        "Available Now"
    )

    st.markdown(
        """
        - Popularity‑Based Recommendations → See what everyone’s watching and join the buzz.

        - Content‑Based Recommendations → Get smart suggestions based on what you already love.

        - Similar Movie Discovery → Find movies that feel just like your favorites.

        - Genre Exploration → Dive deeper into the genres you enjoy — or try something new.

        - Trending Movies → Stay ahead with the films everyone’s talking about right now.

        - Top Rated Movies → Watch the best of the best, hand‑picked by ratings.

        - Hidden Gems → Uncover underrated treasures you might have missed.
        """
    )

with tab2:

    st.info(
        "TV Show recommendation engine is under development."
    )

with tab3:

    st.info(
        "Anime recommendation engine is planned for a future release."
    )

st.divider()


# ==================================================
# Footer
# ==================================================

st.caption(
    """
    NextBinge AI • Entertainment Recommendation Platform

    Powered by Python, Pandas, Scikit-Learn, Streamlit, TMDB Data, and Recommendation System Techniques.
    """
)