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
# Styling (scoped to this page's content + global background overrides)
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    /* Global Background Overrides */
    [data-testid="stAppViewContainer"] {{
        background-color: #FDFBF7 !important;
        background-image: radial-gradient(rgba(139, 90, 43, 0.04) 1px, transparent 1px);
        background-size: 24px 24px;
    }}
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: #F4EAE0 !important;
        border-right: 1px solid rgba(139, 90, 43, 0.1) !important;
    }}
    /* Ensure markdown text outside cards stays dark */
    .stMarkdown p, .stMarkdown li {{
        color: #4A3623 !important;
    }}

    /* Page-Specific UI */
    .hero {{
        padding: 2.8rem 2.5rem 2.4rem 2.5rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #F4EAE0 0%, #FDFBF7 100%);
        border: 1px solid rgba(139, 90, 43, 0.1);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(139, 90, 43, 0.03);
    }}
    .hero::before {{
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(226,209,195,0.5) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }}
    .hero h1 {{
        font-family: 'Fraunces', serif;
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #3E2723;
        position: relative;
        z-index: 1;
    }}
    .hero p {{ 
        color: #7A6652; 
        font-size: 1.1rem; 
        margin: 0; 
        position: relative;
        z-index: 1;
    }}

    /* Book Cards */
    .book-card {{
        background: #FFFFFF;
        border: 1px solid rgba(139, 90, 43, 0.1);
        border-radius: 20px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        height: 100%;
        box-shadow: 0 4px 16px rgba(139, 90, 43, 0.02);
    }}
    .book-card:hover {{
        transform: translateY(-6px);
        border-color: rgba(139, 90, 43, 0.25);
        box-shadow: 0 16px 40px rgba(139, 90, 43, 0.08);
    }}
    .book-cover-wrap {{
        width: 100%;
        aspect-ratio: 2 / 3;
        overflow: hidden;
        border-radius: 12px;
        margin-bottom: 1rem;
        background: #F3EBE1;
        box-shadow: 0 6px 16px rgba(139, 90, 43, 0.06);
    }}
    .book-cover-wrap img {{ width: 100%; height: 100%; object-fit: cover; }}
    
    .book-title {{ 
        font-family: 'Fraunces', serif;
        font-size: 1.1rem; 
        font-weight: 600; 
        line-height: 1.25; 
        margin-bottom: 0.25rem; 
        color: #3E2723;
    }}
    .book-author {{ 
        font-size: 0.85rem; 
        color: #8B7355; 
        margin-bottom: 0.6rem; 
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }}
    .book-desc {{ 
        font-size: 0.9rem; 
        color: #7A6652; 
        line-height: 1.5; 
    }}
    
    .empty-state {{ text-align: center; padding: 4rem 1rem; }}
    .empty-state h3 {{
        font-family: 'Fraunces', serif;
        color: #3E2723;
        margin-bottom: 0.5rem;
        font-size: 1.6rem;
    }}
    .empty-state p {{ color: #8B7355; font-size: 1.1rem; }}
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
                # Updated the fallback placeholder to match the warm theme!
                st.markdown(
                    f"""
                    <div class="book-card">
                        <div class="book-cover-wrap">
                            <img src="{cover}" onerror="this.src='https://placehold.co/400x600/F3EBE1/8B7355?text=No+Cover'"/>
                        </div>
                        <div class="book-title">{row['title']}</div>
                        <div class="book-author">by {authors_str}</div>
                        <div class="book-desc">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )