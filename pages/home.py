import streamlit as st

from core.ui.theme import inject_base_styles, BOOKS, BLOG, BORDER, TEXT_MUTED

inject_base_styles()

# ----------------------------------------------------------------------------
# Page-specific styles: warm floral hero + shelf signature + tactile feature cards
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    /* 1. Force the entire Streamlit app background to a warm floral white */
    [data-testid="stAppViewContainer"] {{
        background-color: #FDFBF7 !important;
        background-image: radial-gradient(rgba(139, 90, 43, 0.04) 1px, transparent 1px);
        background-size: 24px 24px;
    }}
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    /* Warm up the sidebar to match the theme */
    [data-testid="stSidebar"] {{
        background-color: #F4EAE0 !important;
        border-right: 1px solid rgba(139, 90, 43, 0.1) !important;
    }}
    /* Ensure markdown text outside cards stays dark */
    .stMarkdown p, .stMarkdown li {{
        color: #4A3623 !important;
    }}

    /* Hero Section */
    .home-hero {{
        padding: 3.5rem 3rem 2.8rem 3rem;
        border-radius: 28px;
        background: linear-gradient(135deg, #F4EAE0 0%, #FDFBF7 100%);
        border: 1px solid rgba(139, 90, 43, 0.1);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(139, 90, 43, 0.04);
    }}
    
    /* Ambient warm glow in the top right */
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

    .home-hero .eyebrow {{
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.8rem;
        font-weight: 600;
        color: #A68A6D;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }}

    .home-hero h1 {{
        font-family: 'Fraunces', serif;
        font-size: 3.2rem;
        font-weight: 700;
        line-height: 1.15;
        margin-bottom: 0.8rem;
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
    
    .home-hero p.lead {{
        font-size: 1.15rem;
        color: #7A6652 !important;
        max-width: 620px;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }}

    /* Shelf signature */
    .shelf {{
        display: flex;
        align-items: flex-end;
        gap: 8px;
        height: 90px;
        margin-top: 2rem;
        position: relative;
        z-index: 1;
    }}
    .shelf .spine {{
        width: 18px;
        border-radius: 4px 4px 0 0;
        opacity: 0.85;
        transition: transform 0.3s ease;
    }}
    .shelf .spine:hover {{
        transform: translateY(-5px);
    }}
    .shelf-base {{
        height: 4px;
        border-radius: 2px;
        background: rgba(139, 90, 43, 0.15);
        margin-top: 4px;
        position: relative;
        z-index: 1;
    }}

    /* Feature Cards */
    .feature-card {{
        background: #FFFFFF;
        border: 1px solid rgba(139, 90, 43, 0.1);
        border-radius: 24px;
        padding: 2rem 2rem 1.8rem 2rem;
        height: 100%;
        border-left: 4px solid var(--accent);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 8px 24px rgba(139, 90, 43, 0.04);
    }}
    .feature-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 16px 40px rgba(139, 90, 43, 0.08);
    }}
    .feature-card .kicker {{
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--accent);
        margin-bottom: 0.8rem;
    }}
    .feature-card h3 {{
        font-family: 'Fraunces', serif;
        font-size: 1.5rem;
        margin: 0 0 0.8rem 0;
        color: #3E2723;
    }}
    .feature-card p {{
        color: #7A6652;
        font-size: 0.98rem;
        line-height: 1.6;
        margin-bottom: 1.2rem;
    }}
    .feature-card ul {{
        margin: 0 0 1.1rem 0;
        padding-left: 1.2rem;
        color: #8B7355;
        font-size: 0.9rem;
        line-height: 1.8;
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
        <div class="eyebrow">Two tools, one desk</div>
        <h1>Read smarter. <span class="accent">Write faster.</span></h1>
        <p class="lead">
            Inkwell brings together a semantic book recommender and an
            AI blog-writing agent — one for finding your next read, one
            for drafting your next post. Pick a tool below to get started.
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
    st.write("") 
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
    st.write("") 
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