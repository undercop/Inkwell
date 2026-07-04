"""
Shared design tokens for the whole app.

Brand concept: "Inkwell" — a small suite of AI tools for people who read
and write. The palette and type system are shared across every page so
navigating between Home, Book Recommender, and Blog Writer feels like
one product, not three separate demos glued together.

  - BRAND (gold)    → home / shared chrome
  - BOOKS (violet)  → Book Recommender
  - BLOG (coral)    → Blog Writer

Each page keeps its own accent for its hero/cards, but everything else
(background, borders, typography, spacing) is shared from here.
"""

import streamlit as st
APP_NAME = "Inkwell"
APP_TAGLINE = "Your AI reading and writing desk"
BRAND = "#8B5A2B"  # Earthy accent brown
BOOKS = "#C28B5E"  # Warm terracotta/brown
BLOG = "#A68A6D"   # Soft taupe
BORDER = "rgba(139, 90, 43, 0.15)"
TEXT_MUTED = "#7A6652"




BG_DEEP = "#0b0d13"
BG_PANEL = "rgba(255,255,255,0.04)"

TEXT = "#391b14"


_FONTS_AND_BASE_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: radial-gradient(circle at 12% 8%, #171a24 0%, {BG_DEEP} 55%, #08090d 100%);
    color: {TEXT};
}}

h1, h2, h3, .ink-display {{
    font-family: 'Fraunces', serif;
}}

section[data-testid="stSidebar"] {{
    background: #0e1017;
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] * {{
    color: {TEXT};
}}

/* Brand block at the top of the sidebar */
.brand-block {{
    padding: 0.9rem 0.2rem 1rem 0.2rem;
    margin-bottom: 0.4rem;
    border-bottom: 1px solid {BORDER};
}}
.brand-block .brand-name {{
    font-family: 'Fraunces', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: {TEXT};
    letter-spacing: 0.2px;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}}
.brand-block .brand-name .dot {{
    color: {BRAND};
}}
.brand-block .brand-tagline {{
    font-size: 0.8rem;
    color: {TEXT_MUTED};
    margin-top: 0.15rem;
}}

/* Generic card used across pages */
.ink-card {{
    background: {BG_PANEL};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    height: 100%;
}}

/* Section eyebrow label */
.eyebrow {{
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 0.72rem;
    font-weight: 600;
    color: {TEXT_MUTED};
    margin-bottom: 0.5rem;
}}

footer, #MainMenu {{visibility: hidden;}}
</style>
"""


def inject_base_styles() -> None:
    """Call once at the top of every page for a consistent look."""
    st.markdown(_FONTS_AND_BASE_CSS, unsafe_allow_html=True)


def sidebar_brand() -> None:
    """Renders the app name + tagline above the page navigation list."""
    st.sidebar.markdown(
        f"""
        <div class="brand-block">
            <div class="brand-name">🖋️ {APP_NAME}<span class="dot">.</span></div>
            <div class="brand-tagline">{APP_TAGLINE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
