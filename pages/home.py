import streamlit as st

from core.ui.theme import inject_base_styles, BOOKS, BLOG, BORDER, TEXT_MUTED

inject_base_styles()

# ----------------------------------------------------------------------------
# Page-specific styles: hero + shelf signature + feature cards
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .home-hero {{
        padding: 3rem 2.5rem 2.6rem 2.5rem;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(232,179,76,0.10), rgba(139,124,255,0.10) 55%, rgba(255,111,145,0.10));
        border: 1px solid {BORDER};
        margin-bottom: 2rem;
    }}
    .home-hero h1 {{
        font-size: 2.9rem;
        font-weight: 700;
        line-height: 1.12;
        margin-bottom: 0.7rem;
        color: #f5f6fb;
    }}
    .home-hero .accent {{
        background: linear-gradient(90deg, {BOOKS}, {BLOG});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .home-hero p.lead {{
        font-size: 1.08rem;
        color: {TEXT_MUTED};
        max-width: 620px;
        line-height: 1.6;
    }}

    /* Shelf signature: a row of book "spines" of varying height/color */
    .shelf {{
        display: flex;
        align-items: flex-end;
        gap: 6px;
        height: 90px;
        margin-top: 1.8rem;
    }}
    .shelf .spine {{
        width: 16px;
        border-radius: 3px 3px 0 0;
        opacity: 0.85;
    }}
    .shelf-base {{
        height: 4px;
        border-radius: 2px;
        background: {BORDER};
        margin-top: 4px;
    }}

    .feature-card {{
        background: rgba(255,255,255,0.04);
        border: 1px solid {BORDER};
        border-radius: 18px;
        padding: 1.8rem 1.8rem 1.5rem 1.8rem;
        height: 100%;
        border-left: 3px solid var(--accent);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}
    .feature-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.35);
    }}
    .feature-card .kicker {{
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--accent);
        margin-bottom: 0.5rem;
    }}
    .feature-card h3 {{
        font-size: 1.35rem;
        margin: 0 0 0.6rem 0;
        color: #f2f3fa;
    }}
    .feature-card p {{
        color: #c3c5d9;
        font-size: 0.92rem;
        line-height: 1.55;
        margin-bottom: 0.9rem;
    }}
    .feature-card ul {{
        margin: 0 0 1.1rem 0;
        padding-left: 1.1rem;
        color: #b3b6cc;
        font-size: 0.85rem;
        line-height: 1.7;
    }}

    .stack-strip {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.4rem;
    }}
    .stack-pill {{
        border: 1px solid {BORDER};
        color: {TEXT_MUTED};
        border-radius: 999px;
        padding: 0.3rem 0.8rem;
        font-size: 0.78rem;
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
        <div class="eyebrow">Two tools, one desk</div>
        <h1>Read smarter. <span class="accent">Write faster.</span></h1>
        <p class="lead">
            Inkwell brings together a semantic book recommender and an
            AI blog-writing agent — one for finding your next read, one
            for drafting your next post. Pick a tool from the sidebar to
            get started.
        </p>
        <div class="shelf">
            <div class="spine" style="height:60px; background:{BOOKS};"></div>
            <div class="spine" style="height:80px; background:{BLOG};"></div>
            <div class="spine" style="height:45px; background:{BOOKS};"></div>
            <div class="spine" style="height:70px; background:{BOOKS};"></div>
            <div class="spine" style="height:55px; background:{BLOG};"></div>
            <div class="spine" style="height:85px; background:{BOOKS};"></div>
            <div class="spine" style="height:40px; background:{BLOG};"></div>
            <div class="spine" style="height:65px; background:{BLOG};"></div>
        </div>
        <div class="shelf-base"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Feature cards
# ----------------------------------------------------------------------------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        f"""
        <div class="feature-card" style="--accent: {BOOKS};">
            <div class="kicker">📚 Book Recommender</div>
            <h3>Find books by meaning, not keywords</h3>
            <p>
                Describe a mood, theme, or plot in plain language and get
                back real matches — powered by semantic embeddings over
                a catalogue of book descriptions, not string matching.
            </p>
            <ul>
                <li>Search by vibe: "a story about forgiveness"</li>
                <li>Filter by category and emotional tone</li>
                <li>Vector search over embedded book descriptions</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/book_recommender.py", label="Open Book Recommender", icon="📚")

with col2:
    st.markdown(
        f"""
        <div class="feature-card" style="--accent: {BLOG};">
            <div class="kicker">✍️ Blog Writer</div>
            <h3>From topic to draft, with a plan</h3>
            <p>
                Give it a topic and a multi-agent pipeline researches
                (when needed), builds a section-by-section outline, and
                writes a full draft — with citations kept honest.
            </p>
            <ul>
                <li>Routes closed-book vs. research-backed topics</li>
                <li>Plans sections before writing a word</li>
                <li>Parallel section drafting via LangGraph fan-out</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/blog_writer.py", label="Open Blog Writer", icon="✍️")

# ----------------------------------------------------------------------------
# Footer: tech stack strip
# ----------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="eyebrow">Built with</div>
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
