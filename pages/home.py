import streamlit as st
import base64
from pathlib import Path

from core.ui.theme import inject_base_styles, BOOKS, BLOG, BORDER, TEXT_MUTED

inject_base_styles()

# ----------------------------------------------------------------------------
# Image loading helpers
# ----------------------------------------------------------------------------
ASSETS_DIR = Path(__file__).parent.parent / "assets"

def get_base64_image(stem: str) -> tuple[str, str]:
    """Find an asset by filename stem (any common extension) and return
    (base64_string, mime_type)."""
    for ext, mime in [
        (".png", "image/png"),
        (".jpg", "image/jpeg"),
        (".jpeg", "image/jpeg"),
        (".webp", "image/webp"),
        (".svg", "image/svg+xml"),
    ]:
        path = ASSETS_DIR / f"{stem}{ext}"
        if path.exists():
            with open(path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode(), mime
    raise FileNotFoundError(f"No asset found for '{stem}' in {ASSETS_DIR}")

lamp_b64, lamp_mime = get_base64_image("lamp")
manread_b64, manread_mime = get_base64_image("manread")
manpan_b64, manpan_mime = get_base64_image("manpan")

# ----------------------------------------------------------------------------
# Page-specific styles
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
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
    .stMarkdown p, .stMarkdown li {{
        color: #4A3623 !important;
    }}

    /* Hero Section */
    .home-hero {{
        padding: 2.6rem 3rem 2.4rem 3rem;
        border-radius: 28px;
        background: linear-gradient(135deg, #F4EAE0 0%, #FDFBF7 100%);
        border: 1px solid rgba(139, 90, 43, 0.1);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(139, 90, 43, 0.04);
    }}
    .home-hero::before {{
        content: "";
        position: absolute;
        top: -40%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(226,209,195,0.6) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }}
    .home-hero .eyebrow-row {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.9rem;
        position: relative;
        z-index: 1;
    }}
    .home-hero .eyebrow-row img {{
        width: 22px;
        height: 22px;
        object-fit: contain;
    }}
    .home-hero .eyebrow {{
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.8rem;
        font-weight: 600;
        color: #A68A6D;
        position: relative;
        z-index: 1;
    }}
    .home-hero h1 {{
        font-family: 'Fraunces', serif;
        font-size: 2.6rem;
        font-weight: 700;
        line-height: 1.15;
        margin-bottom: 0;
        color: #3E2723;
        position: relative;
        z-index: 1;
        letter-spacing: -0.5px;
    }}
    .home-hero .accent {{
        background: linear-gradient(90deg, #8B5A2B, #C28B5E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* ---------------- Outer card containers (one box each) ---------------- */
    /* These wrap BOTH the markdown content and the button below it, so the
       shadow/border/radius apply once to the whole unit with no seam. */
    div[class*="st-key-card-book"] {{
        background: #FFFFFF;
        border: 1px solid rgba(139, 90, 43, 0.1);
        border-left: 5px solid {BOOKS};
        border-radius: 24px;
        overflow: hidden;
        box-shadow: -14px 10px 32px rgba(139, 90, 43, 0.16), 0 8px 24px rgba(139, 90, 43, 0.05);
    }}
    div[class*="st-key-card-blog"] {{
        background: #FFFFFF;
        border: 1px solid rgba(139, 90, 43, 0.1);
        border-left: 5px solid {BLOG};
        border-radius: 24px;
        overflow: hidden;
        box-shadow: -14px 10px 32px rgba(139, 90, 43, 0.16), 0 8px 24px rgba(139, 90, 43, 0.05);
    }}

    /* Inner text/illustration block — no border/shadow of its own now,
       the outer container owns those. */
    .feature-card {{
        padding: 1.8rem 1.8rem 0.5rem 1.8rem;   /* was 0 on bottom, now small gap before button */
    display: flex;
    flex-direction: column;
    }}
    .feature-card .kicker {{
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--accent);
        margin-bottom: 0.7rem;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }}
    .feature-card h3 {{
        font-family: 'Fraunces', serif;
        font-size: 1.5rem;
        margin: 0 0 0.7rem 0;
        color: #3E2723;
        flex-shrink: 0;
        line-height: 1.25;
    }}
    .feature-card p {{
        color: #7A6652;
        font-size: 0.98rem;
        line-height: 1.6;
        margin-bottom: 0;
        flex-shrink: 0;
    }}

    /* Illustration area — big, bottom-anchored */
    .feature-card .illustration-wrap {{
        flex: 1 1 auto;
        min-height: 260px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        margin-top: 0.5rem;
    }}
    .feature-card .illustration-wrap img {{
        max-width: 100%;
        max-height: 320px;
        width: auto;
        height: auto;
        object-fit: contain;
    }}

    /* The "Open X" link, styled as a full-width button flush to the box bottom */
    div[class*="st-key-card-book"] [data-testid="stPageLink"],
    div[class*="st-key-card-blog"] [data-testid="stPageLink"] {{
         display: flex;
    justify-content: center;
    width: 100%;
    padding: 0 1.8rem 1.8rem 1.8rem;   /* space on all sides around the button */
    margin-top: 0.5rem;
    box-sizing: border-box;
    }}
    div[class*="st-key-card-book"] [data-testid="stPageLink"] a {{
        display: flex !important;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    width: 100%;
    max-width: 320px;              /* keeps it from stretching edge to edge */
    box-sizing: border-box;
    background: {BOOKS} !important;
    color: #FFFFFF !important;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.9rem 1.5rem;
    border-radius: 14px !important;   /* own rounded corners, no longer 0 */
    border: none !important;
    text-decoration: none !important;
    transition: filter 0.2s ease, transform 0.2s ease;
    }}
    div[class*="st-key-card-blog"] [data-testid="stPageLink"] a {{
        display: flex !important;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    width: 100%;
    max-width: 320px;
    box-sizing: border-box;
    background: {BLOG} !important;
    color: #FFFFFF !important;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.9rem 1.5rem;
    border-radius: 14px !important;
    border: none !important;
    text-decoration: none !important;
    transition: filter 0.2s ease, transform 0.2s ease;
    }}
    div[class*="st-key-card-book"] [data-testid="stPageLink"] a:hover,
    div[class*="st-key-card-blog"] [data-testid="stPageLink"] a:hover {{
        filter: brightness(1.08);
    transform: translateY(-1px);
    }}
    div[class*="st-key-card-book"] [data-testid="stPageLink"] a p,
    div[class*="st-key-card-blog"] [data-testid="stPageLink"] a p {{
        color: #FFFFFF !important;
    margin: 0 !important;
    font-weight: 600;
    }}

    /* Footer Tech Stack */
    .stack-strip {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 0.6rem;
    }}
    .stack-pill {{
        background: #FFFFFF;
        border: 1px solid rgba(139, 90, 43, 0.15);
        color: #7A6652;
        border-radius: 999px;
        padding: 0.35rem 1rem;
        font-size: 0.82rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(139, 90, 43, 0.02);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="home-hero">
        <div class="eyebrow-row">
            <img src="data:{lamp_mime};base64,{lamp_b64}" alt="Lamp" />
            <div class="eyebrow">One desk, two tools</div>
        </div>
        <h1>Read smarter. <span class="accent">Write faster.</span></h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Feature cards — each is ONE outer container holding markdown + button
# ----------------------------------------------------------------------------
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(key="card-book"):
        st.markdown(
            f"""
            <div class="feature-card" style="--accent: {BOOKS};">
                <div class="kicker">📚 Book Recommender</div>
                <h3>Find books by meaning,<br>not keywords</h3>
                <p>
                    Describe a mood, theme, or plot in plain language and get
                    back real matches — powered by semantic embeddings over
                    a catalogue of book descriptions, not string matching.
                </p>
                <div class="illustration-wrap">
                    <img src="data:{manread_mime};base64,{manread_b64}" alt="Reading illustration" />
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/book_recommender.py", label="Open Book Recommender", icon="📖")

with col2:
    with st.container(key="card-blog"):
        st.markdown(
            f"""
            <div class="feature-card" style="--accent: {BLOG};">
                <div class="kicker">✍️ Blog Writer</div>
                <h3>From topic to draft,<br>with a plan</h3>
                <p>
                    Give it a topic and a multi-agent pipeline researches
                    (when needed), builds a section-by-section outline, and
                    writes a full draft — with citations kept honest.
                </p>
                <div class="illustration-wrap">
                    <img src="data:{manpan_mime};base64,{manpan_b64}" alt="Writing illustration" />
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/blog_writer.py", label="Open Blog Writer", icon="✍️")

# ----------------------------------------------------------------------------
# Footer: tech stack strip
# ----------------------------------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="eyebrow" style="text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.8rem; font-weight: 600; color: #A68A6D; margin-bottom: 0.4rem;">Built with</div>
    <div class="stack-strip">
        <span class="stack-pill">Streamlit</span>
        <span class="stack-pill">LangChain</span>
        <span class="stack-pill">LangGraph</span>
        <span class="stack-pill">Chroma</span>
        <span class="stack-pill">Sentence-Transformers</span>
        <span class="stack-pill">Groq · Llama 3.3</span>
        <span class="stack-pill">Tavily</span>
    </div>
    """,
    unsafe_allow_html=True,
)