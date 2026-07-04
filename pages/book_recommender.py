import streamlit as st

from core.book_recommender.data import load_data_and_db
from core.book_recommender.recommend import (
    retrieve_semantic_recommendations,
    format_authors,
    truncate_description,
)
from core.ui.theme import inject_base_styles, BOOKS, BORDER

inject_base_styles()

# ----------------------------------------------------------------------------
# Styling (scoped to this page's content, using the shared "BOOKS" accent)
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .hero {{
        padding: 2.2rem 2rem 1.6rem 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, {BOOKS}22, {BOOKS}08);
        border: 1px solid {BORDER};
        margin-bottom: 1.6rem;
    }}
    .hero h1 {{
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #f2f3fa;
    }}
    .hero p {{ color: #b8bcd0; font-size: 1.0rem; margin: 0; }}

    .book-card {{
        background: rgba(255,255,255,0.04);
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 0.8rem;
        margin-bottom: 1.2rem;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        height: 100%;
    }}
    .book-card:hover {{
        transform: translateY(-4px);
        border-color: {BOOKS}80;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
    .book-cover-wrap {{
        width: 100%;
        aspect-ratio: 2 / 3;
        overflow: hidden;
        border-radius: 10px;
        margin-bottom: 0.6rem;
        background: #1c1e29;
    }}
    .book-cover-wrap img {{ width: 100%; height: 100%; object-fit: cover; }}
    .book-title {{ font-size: 0.98rem; font-weight: 600; line-height: 1.25; margin-bottom: 0.15rem; }}
    .book-author {{ font-size: 0.82rem; color: #9b9fc2; margin-bottom: 0.4rem; }}
    .book-desc {{ font-size: 0.8rem; color: #c3c5d9; line-height: 1.4; }}
    .empty-state {{ text-align: center; padding: 3rem 1rem; color: #8b8fae; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>📚 Semantic Book Recommender</h1>
        <p>Describe a vibe, theme, or plot — get book recommendations matched by meaning, not just keywords.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Load data (cached — instant after the first run of the server process)
# ----------------------------------------------------------------------------
books, db_books = load_data_and_db()

CATEGORIES = ["All"] + sorted(books["simple_categories"].unique())
TONES = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]

# ----------------------------------------------------------------------------
# Sidebar controls
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🔍 Find your next read")
    query = st.text_area(
        "Describe the kind of book you're looking for",
        placeholder="e.g., A story about forgiveness and second chances",
        height=100,
        key="book_query",
    )
    category = st.selectbox("Category", CATEGORIES, index=0, key="book_category")
    tone = st.selectbox("Emotional tone", TONES, index=0, key="book_tone")
    n_results = st.slider("Number of recommendations", min_value=4, max_value=24, value=16, step=4, key="book_n")
    search_clicked = st.button("✨ Find recommendations", key="book_search_btn")

# ----------------------------------------------------------------------------
# Session state so results persist across reruns / page switches
# ----------------------------------------------------------------------------
if "book_results" not in st.session_state:
    st.session_state.book_results = None

if search_clicked:
    if not query.strip():
        st.warning("Please enter a short description of the book you're looking for.")
    else:
        with st.spinner("Searching the shelves…"):
            st.session_state.book_results = retrieve_semantic_recommendations(
                db_books, books, query, category, tone, final_top_k=n_results
            )

results = st.session_state.book_results

if results is None:
    st.markdown(
        """
        <div class="empty-state">
            <h3>👋 Enter a description in the sidebar to get started</h3>
            <p>Try something like <em>"a cozy mystery set in a small town"</em>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif results.empty:
    st.markdown(
        """
        <div class="empty-state">
            <h3>😕 No matches found</h3>
            <p>Try a different description, category, or tone.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(f"### Recommendations ({len(results)})")
    cols_per_row = 4
    rows = [results.iloc[i : i + cols_per_row] for i in range(0, len(results), cols_per_row)]

    for row_chunk in rows:
        cols = st.columns(cols_per_row)
        for col, (_, row) in zip(cols, row_chunk.iterrows()):
            with col:
                authors_str = format_authors(row["authors"])
                desc = truncate_description(row["description"])
                cover = row["large_thumbnail"]
                st.markdown(
                    f"""
                    <div class="book-card">
                        <div class="book-cover-wrap">
                            <img src="{cover}" onerror="this.src='https://placehold.co/400x600/1c1e29/8b8fae?text=No+Cover'"/>
                        </div>
                        <div class="book-title">{row['title']}</div>
                        <div class="book-author">by {authors_str}</div>
                        <div class="book-desc">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
