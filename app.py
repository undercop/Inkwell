"""
Single entry point for the merged app.

Run with:
    streamlit run app.py

Auth flow:
  - core.auth.session.ensure_session() checks for a logged-in Supabase
    session (restoring from a browser cookie if needed).
  - If not logged in: render the standalone login/signup screen
    (core.auth.ui.render_auth_page) and stop — no sidebar, no nav, no
    access to any other page.
  - If logged in: show sidebar branding + nav, defaulting to Home.
"""
import streamlit as st

from core.ui.theme import inject_base_styles, sidebar_brand, APP_NAME
from core.auth.session import ensure_session, clear_session
from core.auth.ui import render_auth_page

st.set_page_config(
    page_title=f"{APP_NAME} — Book Recommender & Blog Writer",
    page_icon="🌿", # Updated to fit the organic/floral theme
    layout="wide",
    initial_sidebar_state="expanded",
)

session = ensure_session()

if session is None:
    render_auth_page()
    st.stop()

# ----------------------------------------------------------------------------
# Logged in — sidebar branding + nav. Nothing above this point renders any
# app page, so there's no way to reach Book Recommender / Blog Writer
# without a valid session.
# ----------------------------------------------------------------------------
inject_base_styles()
sidebar_brand()

with st.sidebar:
    st.caption(f"Signed in as **{session.email}**")
    if st.button("Log out", use_container_width=True):
        clear_session()
        st.rerun()

pages = {
    "": [
        st.Page("pages/home.py", title="Home", icon = "🌸", default=True),
    ],
    "Tools": [
        st.Page("pages/book_recommender.py", title="Book Recommender"),
        st.Page("pages/blog_writer.py", title="Blog Writer"),
    ],
}

pg = st.navigation(pages)
pg.run()