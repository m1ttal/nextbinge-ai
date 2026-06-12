from pathlib import Path

import joblib
import pandas as pd
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

 
MOVIES_MODEL_DIR = PROJECT_ROOT / "models" / "movies"

from sklearn.feature_extraction.text import TfidfVectorizer

from src.data.loaders import load_movie_master

def build_tfidf_matrix(
    movie_master: pd.DataFrame,
    max_features: int = 20000
):
    """
    Build TF-IDF matrix from content_text.
    """

    if "content_text" not in movie_master.columns:
        raise ValueError(
            "'content_text' column not found."
        )

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=max_features,
        strip_accents="unicode",
        lowercase=True
    )

    tfidf_matrix = vectorizer.fit_transform(
        movie_master["content_text"]
        .fillna("")
    )

    return vectorizer, tfidf_matrix


def build_item_lookup(
    movie_master: pd.DataFrame
) -> pd.Series:
    """
    Build item_id -> dataframe index lookup.
    """

    return pd.Series(
        movie_master.index,
        index=movie_master["item_id"]
    )


def train_content_model(
    movie_master: pd.DataFrame,
):
    """
    Train and save content-based artifacts.
    """

    vectorizer, tfidf_matrix = (
        build_tfidf_matrix(
            movie_master
        )
    )

    item_lookup = build_item_lookup(
        movie_master
    )

    joblib.dump(
        vectorizer,
        MOVIES_MODEL_DIR / "tfidf_vectorizer.pkl"
    )

    joblib.dump(
        tfidf_matrix,
        MOVIES_MODEL_DIR / "tfidf_matrix.pkl"
    )

    joblib.dump(
        item_lookup,
        MOVIES_MODEL_DIR / "item_lookup.pkl"
    )

    print(
        "Content model artifacts saved."
    )


if __name__ == "__main__":
    movie_master = load_movie_master()
    train_content_model(movie_master)
