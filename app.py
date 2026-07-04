"""
Single entry point for the merged app.

Run with:
    streamlit run app.py

This file ONLY sets up page config, sidebar branding, and navigation.
All real logic lives in core/ (no Streamlit calls) and pages/ (UI only,
imports from core/).
"""
import streamlit as st

from core.ui.theme import inject_base_styles, sidebar_brand, APP_NAME

st.set_page_config(
    page_title=f"{APP_NAME} — Book Recommender & Blog Writer",
    page_icon="🖋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_base_styles()
sidebar_brand()

pages = {
    "": [
        st.Page("pages/home.py", title="Home", icon="🏠", default=True),
    ],
    "Tools": [
        st.Page("pages/book_recommender.py", title="Book Recommender", icon="📚"),
        st.Page("pages/blog_writer.py", title="Blog Writer", icon="✍️"),
    ],
}

pg = st.navigation(pages)
pg.run()
