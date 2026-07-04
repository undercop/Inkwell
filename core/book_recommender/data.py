"""
Data + vector store loading for the book recommender.

This is the piece that made stream-dash.py slow: previously the app
re-embedded tagged_description.txt into a fresh in-memory Chroma DB on
every cold start. Here we:

  1. Prefer a *persisted* Chroma DB on disk (built once by
     scripts/build_vector_db.py) — loading this is fast.
  2. Fall back to building it in-memory if no persisted DB is found,
     so the app still works out of the box on a fresh clone.

Everything here is cached with st.cache_resource so it only runs once
per Streamlit server process, regardless of which page or how many
times the user interacts with widgets.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root
DATA_DIR = BASE_DIR / "data"

BOOKS_CSV = DATA_DIR / "books_with_emotions.csv"
TAGGED_DESCRIPTIONS = DATA_DIR / "tagged_description.txt"
FALLBACK_COVER = DATA_DIR / "cover-not-found.jpg"
CHROMA_PERSIST_DIR = DATA_DIR / "chroma_db"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@st.cache_resource(show_spinner="Loading book catalogue…")
def load_books() -> pd.DataFrame:
    books = pd.read_csv(BOOKS_CSV)
    books["large_thumbnail"] = books["thumbnail"] + "&fife=w800"
    books["large_thumbnail"] = np.where(
        books["large_thumbnail"].isna(),
        str(FALLBACK_COVER),
        books["large_thumbnail"],
    )
    return books


@st.cache_resource(show_spinner="Loading embedding model…")
def load_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


@st.cache_resource(show_spinner="Loading vector index…")
def load_vector_db() -> Chroma:
    embeddings = load_embeddings()

    if CHROMA_PERSIST_DIR.exists() and any(CHROMA_PERSIST_DIR.iterdir()):
        # Fast path: load the pre-built index from disk.
        return Chroma(
            persist_directory=str(CHROMA_PERSIST_DIR),
            embedding_function=embeddings,
        )

    # Slow path: no persisted DB found, build one in memory.
    # (Run scripts/build_vector_db.py once to avoid this on every launch.)
    raw_documents = TextLoader(str(TAGGED_DESCRIPTIONS), encoding="utf-8").load()
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=0, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)
    return Chroma.from_documents(documents, embeddings)


def load_data_and_db():
    """Convenience helper used by the page: returns (books_df, chroma_db)."""
    return load_books(), load_vector_db()
