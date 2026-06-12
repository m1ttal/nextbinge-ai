from pathlib import Path

import pandas as pd
import fastparquet
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "processed" / "movies"

MOVIES_MODEL_DIR = PROJECT_ROOT / "models" / "movies"


# =========================
# Movies
# =========================

def load_item_genres() -> pd.DataFrame:
    """
    Load normalized movie genres.
    """

    file_path = (
        DATA_DIR
        / "item_genres.parquet"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return pd.read_parquet(file_path)

def load_movie_master() -> pd.DataFrame:
    """
    Load the master movie feature store.

    Returns
    -------
    pd.DataFrame
        Movie metadata + recommendation features.
    """

    file_path = (
        DATA_DIR
        / "movie_master.parquet"
    )

    return pd.read_parquet(file_path)


def load_movie_content_artifacts():
    """
    Load trained content-based recommendation artifacts.
    """

    tfidf_matrix = joblib.load(
        MOVIES_MODEL_DIR
        / "tfidf_matrix.pkl"
    )

    item_lookup = joblib.load(
        MOVIES_MODEL_DIR
        / "item_lookup.pkl"
    )

    return (
        tfidf_matrix,
        item_lookup
    )