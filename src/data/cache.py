import streamlit as st
import pandas as pd

from .loaders import (
    load_item_genres,
    load_movie_master,
    load_movie_content_artifacts
)


@st.cache_data
def get_item_genres() -> pd.DataFrame:
    return load_item_genres()

@st.cache_data
def get_movie_master() -> pd.DataFrame:
    return load_movie_master()

@st.cache_resource
def get_movie_content_artifacts():
    return load_movie_content_artifacts()