"""
Run this ONCE (or whenever tagged_description.txt changes) to build
a persisted Chroma vector database.

Usage:
    python scripts/build_vector_db.py
"""

from pathlib import Path
import shutil

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TAGGED_DESCRIPTIONS = DATA_DIR / "tagged_description.txt"
CHROMA_PERSIST_DIR = DATA_DIR / "chroma_db"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# -------------------------------------------------
# Build Vector DB
# -------------------------------------------------

def main():

    if not TAGGED_DESCRIPTIONS.exists():
        raise FileNotFoundError(
            f"{TAGGED_DESCRIPTIONS} not found.\n"
            "Make sure tagged_description.txt exists inside the data folder."
        )

    print("=" * 60)
    print("Loading descriptions...")
    print("=" * 60)

    raw_documents = TextLoader(
        str(TAGGED_DESCRIPTIONS),
        encoding="utf-8",
    ).load()

    # Entire file contents
    text = raw_documents[0].page_content

    # One document per line
    documents = [
        Document(page_content=line.strip())
        for line in text.splitlines()
        if line.strip()
    ]

    print(f"Loaded {len(documents)} book descriptions.")

    print("\nLoading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )

    # Remove previous DB
    if CHROMA_PERSIST_DIR.exists():
        print("Removing existing Chroma database...")
        shutil.rmtree(CHROMA_PERSIST_DIR)

    CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

    print("\nCreating vector database...")
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(CHROMA_PERSIST_DIR),
    )

    print("\nDone!")
    print(f"Saved database to:\n{CHROMA_PERSIST_DIR}")


if __name__ == "__main__":
    main()