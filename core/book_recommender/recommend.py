"""
Recommendation logic — kept free of any `st.*` calls so it can be
imported, tested, or reused (e.g. from a future API) independently of
the Streamlit UI.
"""
import pandas as pd
from langchain_chroma import Chroma

TONE_TO_COLUMN = {
    "Happy": "joy",
    "Surprising": "surprise",
    "Angry": "anger",
    "Suspenseful": "fear",
    "Sad": "sadness",
}


def retrieve_semantic_recommendations(
    db_books: Chroma,
    books: pd.DataFrame,
    query: str,
    category: str = "All",
    tone: str = "All",
    initial_top_k: int = 50,
    final_top_k: int = 16,
) -> pd.DataFrame:
    recs = db_books.similarity_search(query, k=initial_top_k)
    books_list = [int(rec.page_content.strip('"').split()[0]) for rec in recs]
    book_recs = books[books["isbn13"].isin(books_list)].head(initial_top_k)

    if category != "All":
        book_recs = book_recs[book_recs["simple_categories"] == category].head(final_top_k)
    else:
        book_recs = book_recs.head(final_top_k)

    tone_column = TONE_TO_COLUMN.get(tone)
    if tone_column:
        book_recs = book_recs.sort_values(by=tone_column, ascending=False)

    return book_recs


def format_authors(authors_field: str) -> str:
    authors_split = str(authors_field).split(";")
    if len(authors_split) == 2:
        return f"{authors_split[0]} and {authors_split[1]}"
    elif len(authors_split) > 2:
        return f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
    return authors_field


def truncate_description(description: str, word_limit: int = 24) -> str:
    words = str(description).split()
    if len(words) <= word_limit:
        return description
    return " ".join(words[:word_limit]) + "…"
