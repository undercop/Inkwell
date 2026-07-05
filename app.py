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
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

session = ensure_session()

if session is None:
    render_auth_page()
    st.stop()

# ----------------------------------------------------------------------------
# Logged in — sidebar order: brand -> nav -> page-specific content -> logout
# ----------------------------------------------------------------------------
inject_base_styles()

# 1. Branding at the very top
sidebar_brand()

# 2. Nav menu (Home + Tools) right under the brand
pages = {
    "": [
        st.Page("pages/home.py", title="Home", icon=":material/home:", default=True),
    ],
    "Tools": [
        st.Page("pages/book_recommender.py", title="Book Recommender", icon=":material/menu_book:"),
        st.Page("pages/blog_writer.py", title="Blog Writer", icon=":material/edit:"),
    ],
}
pg = st.navigation(pages)

# 3. Run the selected page — any page-specific sidebar widgets (filters,
#    settings, etc.) that a page adds via `st.sidebar` will render here,
#    below the nav and above the logout block, since it executes now.
pg.run()

# 4. Signed-in info + logout, pinned to the bottom
with st.sidebar:
    st.divider()
    st.caption(f"Signed in as **{session.email}**")
    if st.button("Log out", use_container_width=True):
        clear_session()
        st.rerun()