import streamlit as st

from core.auth.service import sign_up, sign_in
from core.auth.session import persist_session
from core.ui.theme import inject_base_styles, APP_NAME, APP_TAGLINE, BRAND, BOOKS, BLOG

import base64
from pathlib import Path

def get_base64_image(image_path: str) -> str:
    """Read an image file and return a base64-encoded string."""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Resolve paths relative to this script's location (safer than "../assets/...")
ASSETS_DIR = Path(__file__).parent.parent.parent / "assets"

lamp_b64 = get_base64_image(ASSETS_DIR / "lamp.png")
login_b64 = get_base64_image(ASSETS_DIR / "login.jpg")

def _hide_app_chrome() -> None:
    """This page has no sidebar / nav — hide the (otherwise empty) sidebar
    and its collapse arrow so it reads as a distinct, standalone screen."""
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] { display: none; }
        [data-testid="collapsedControl"] { display: none; }
        .block-container { padding-top: 2rem !important; max-width: 1000px !important; z-index: 2; position: relative; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _auth_page_styles() -> None:
    st.markdown(
        f"""
        <style>
        /* 1. Force the entire Streamlit app background to a warm floral white */
        [data-testid="stAppViewContainer"] {{
            background-color: #FDFBF7 !important;
        }}
        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}

        /* ------------------------------------------------------------------ */
        /* FLOATING SQUARES BACKGROUND ANIMATION (Converted from SCSS)        */
        /* ------------------------------------------------------------------ */
        .auth-bg-animation {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: 0;
            overflow: hidden;
            background-color: #FDFBF7;
            pointer-events: none; /* Let clicks pass through to the form */
        }}
        
        .auth-bg-animation:before {{ 
            z-index: 1000;
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 60vh;
            background-image: linear-gradient(180deg, #FDFBF7 0%, rgba(253,251,247,0.00) 100%);
        }}
        
        .auth-bg-animation:after {{ 
            z-index: 1000;
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 20vh;
            background-image: linear-gradient(0deg, #F4EAE0 0%, rgba(244,234,224,0.00) 100%);
        }}

        .squares {{
            height: 100%;
            display: flex;
            justify-content: space-around;
            overflow: hidden;
            margin: 0; padding: 0;
        }}

        .square {{
            animation: squares 9.5s linear infinite;
            align-self: flex-end;
            width: 1em;
            height: 1em;
            transform: translateY(100%);
            /* Adapted to warm floral theme */
            background: rgba(139, 90, 43, 0.08);  
        }}
        
        .square:nth-child(2) {{ height: 1.5em; width: 3em; animation-delay: 1s; animation-duration: 17s; filter: blur(5px); -webkit-filter: blur(5px); }}
        .square:nth-child(3) {{ height: 2em; width: 1em; animation-delay: 1.5s; animation-duration: 8s; filter: blur(0px); -webkit-filter: blur(0px); }}
        .square:nth-child(4) {{ height: 1em; width: 1.5em; animation-delay: 0.5s; animation-duration: 13s; filter: blur(3px); -webkit-filter: blur(3px); }}
        .square:nth-child(5) {{ height: 1.25em; width: 2em; animation-delay: 4s; animation-duration: 11s; filter: blur(2px); -webkit-filter: blur(2px); }}
        .square:nth-child(6) {{ height: 2.5em; width: 2em; animation-delay: 2s; animation-duration: 9s; filter: blur(1px); -webkit-filter: blur(1px); }}
        .square:nth-child(7) {{ height: 5em; width: 2em; filter: blur(2.5px); -webkit-filter: blur(2.5px); animation-duration: 12s; }}
        .square:nth-child(8) {{ height: 1em; width: 3em; animation-delay: 5s; animation-duration: 18s; filter: blur(6px); -webkit-filter: blur(6px); }}
        .square:nth-child(9) {{ height: 1.5em; width: 2em; filter: blur(0.5px); -webkit-filter: blur(0.5px); animation-duration: 9s; }}
        .square:nth-child(10) {{ height: 3em; width: 2.4em; animation-delay: 6s; filter: blur(0.5px); -webkit-filter: blur(0.5px); animation-duration: 12s; }}

        @keyframes squares {{ 
            from {{ transform: translateY(100%) rotate(-50deg); }}
            to   {{ transform: translateY(calc(-100vh + -100%)) rotate(20deg); }}
        }}

        /* ------------------------------------------------------------------ */
        /* UI CARDS AND BRANDING PANELS                                       */
        /* ------------------------------------------------------------------ */
        .auth-brand-panel {{
            background: linear-gradient(135deg, #F4EAE0 0%, #E8D8C8 100%);
            border: 2px solid #FFFFFF;
            padding: 2.5rem 2rem 2rem;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            height: 100%;
            min-height: 520px;
            border-radius: 32px;
            box-shadow: 0 20px 40px rgba(139, 90, 43, 0.08);
            position: relative;
            overflow: hidden;
            z-index: 5;
        }}
        
        .auth-brand-panel::before {{
            content: "";
            position: absolute;
            top: -20%; left: -10%;
            width: 300px; height: 300px;
            background: radial-gradient(circle, rgba(253,251,247,0.9) 0%, transparent 70%);
            border-radius: 50%; pointer-events: none;
        }}
        .auth-brand-panel::after {{
            content: "";
            position: absolute;
            bottom: -15%; right: -15%;
            width: 320px; height: 320px;
            background: radial-gradient(circle, rgba(226,209,195,0.85) 0%, transparent 70%);
            border-radius: 50%; pointer-events: none;
        }}
        
        .brand-title-row {{
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 0.3rem;
            z-index: 1;
            flex-shrink: 0;
        }}
        .brand-title-row img {{
            width: 54px;
            height: auto;
            border-radius: 16px;
            box-shadow: 0 10px 24px rgba(139, 90, 43, 0.12);
        }}
        .brand-mark {{
            font-family: 'Fraunces', serif;
            font-size: 2.6rem;
            font-weight: 700;
            color: #4A3623;
            margin-bottom: 0;
            z-index: 1;
            letter-spacing: -0.5px;
        }}
        .brand-mark .dot {{ color: {BRAND}; }}
        
        .brand-sub {{
            color: #7A6652;
            font-size: 1.05rem;
            max-width: 320px;
            line-height: 1.5;
            margin-bottom: 0.75rem;
            z-index: 1;
            flex-shrink: 0;
        }}

        /* tagline directly under the title — tighter bottom margin before the image */
        .brand-title-row + .brand-sub {{
            margin-bottom: 1rem;
        }}

        /* the image now grows to fill remaining vertical space in the panel */
        .brand-illustration {{
             width: 100%;
    flex: 1 1 auto;
    min-height: 0;
    max-width: 100%;
    height: auto;
    max-height: 320px;
    object-fit: cover;
    border-radius: 20px;
    margin: 0.5rem 0;
    position: relative;
    filter: drop-shadow(0 8px 20px rgba(139, 90, 43, 0.10));

    /* fade all edges evenly into the panel background */
    -webkit-mask-image: radial-gradient(ellipse 75% 60% at center, black 60%, transparent 100%);
    mask-image: radial-gradient(ellipse 75% 90% at center, black 60%, transparent 100%);
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    -webkit-mask-size: 100% 100%;
    mask-size: 100% 100%;
    z-index: 1;
        }}

        /* closing caption — own flex row below the image, can't overlap it */
        .brand-sub.brand-caption {{
            margin-top: 0.75rem;
            margin-bottom: 0;
            flex-shrink: 0;
        }}
        
        .auth-shelf {{
            display: flex;
            align-items: flex-end;
            gap: 8px;
            height: 70px;
            z-index: 1;
        }}
        .auth-shelf .spine {{ 
            width: 16px; 
            border-radius: 4px 4px 0 0; 
            opacity: 0.85; 
            transition: transform 0.3s ease, opacity 0.3s ease; 
        }}
        .auth-shelf .spine:hover {{ transform: translateY(-6px); opacity: 1; }}

        h2.auth-header {{
            font-family: 'Fraunces', serif;
            font-size: 2.2rem !important;
            margin-bottom: 0.2rem !important;
            padding-bottom: 0 !important;
            color: #3E2723;
        }}
        p.auth-sub {{
            color: #8B7355;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }}

        [data-testid="stForm"] {{
            background: #FFFFFF !important;
            border: 1px solid rgba(139, 90, 43, 0.1) !important;
            border-radius: 24px !important;
            padding: 2rem !important;
            box-shadow: 0 12px 30px rgba(139, 90, 43, 0.05) !important;
            transition: box-shadow 0.3s ease;
            z-index: 5;
            position: relative;
        }}
        [data-testid="stForm"]:hover {{
            box-shadow: 0 16px 40px rgba(139, 90, 43, 0.08) !important;
        }}
        
        .stTextInput input {{
            color: #3E2723 !important;
            background-color: #FDFBF7 !important;
            border-radius: 12px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _toggle_row(mode: str) -> None:
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Log in",
            key="auth_toggle_login",
            use_container_width=True,
            type="primary" if mode == "login" else "secondary",
        ):
            st.session_state.auth_mode = "login"
            st.rerun()
    with col2:
        if st.button(
            "Sign up",
            key="auth_toggle_signup",
            use_container_width=True,
            type="primary" if mode == "signup" else "secondary",
        ):
            st.session_state.auth_mode = "signup"
            st.rerun()


def render_auth_page() -> None:
    inject_base_styles()
    _hide_app_chrome()
    _auth_page_styles()

    # ------------------------------------------------------------------
    # INJECT HTML FOR BACKGROUND ANIMATION
    # ------------------------------------------------------------------
    st.markdown("""
        <div class="auth-bg-animation">
            <div class="squares">
                <div class="square"></div>
                <div class="square"></div>
                <div class="square"></div>
                <div class="square"></div>
                <div class="square"></div>
                <div class="square"></div>
                <div class="square"></div>
                <div class="square"></div>
                <div class="square"></div>
                <div class="square"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"
    mode = st.session_state.auth_mode

    left, right = st.columns([1.1, 1], gap="large")

    with left:
        st.markdown(
            f"""
            <div class="auth-brand-panel">
                <div class="brand-title-row">
                    <img src="data:image/png;base64,{lamp_b64}" alt="Lamp logo" />
                    <div class="brand-mark">{APP_NAME}<span class="dot">.</span></div>
                </div>
                <div class="brand-sub">{APP_TAGLINE}</div>
                <img class="brand-illustration" src="data:image/jpeg;base64,{login_b64}" alt="Login illustration" />
                <div class="brand-sub brand-caption">Sign in to find your next read or draft your next post.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.write("")  # Slight vertical balance

        if mode == "login":
            st.markdown("<h2 class='auth-header'>Welcome back</h2>", unsafe_allow_html=True)
            st.markdown("<p class='auth-sub'>Log in to continue.</p>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 class='auth-header'>Create account</h2>", unsafe_allow_html=True)
            st.markdown("<p class='auth-sub'>Takes less than a minute.</p>", unsafe_allow_html=True)

        _toggle_row(mode)
        st.write("")

        if mode == "login":
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                submitted = st.form_submit_button("Log in", use_container_width=True, type="primary")

            if submitted:
                if not email or not password:
                    st.warning("Please enter both email and password.")
                else:
                    with st.spinner("Signing in…"):
                        session, error = sign_in(email.strip(), password)
                    if session:
                        persist_session(session)
                        st.session_state.pop("auth_mode", None)
                        st.rerun()
                    else:
                        st.error(error)

        else:
            with st.form("signup_form", clear_on_submit=False):
                email = st.text_input("Email", key="signup_email")
                password = st.text_input("Password", type="password", key="signup_password")
                confirm = st.text_input("Confirm password", type="password", key="signup_confirm")
                submitted = st.form_submit_button("Create account", use_container_width=True, type="primary")

            if submitted:
                if not email or not password:
                    st.warning("Please fill in every field.")
                elif password != confirm:
                    st.warning("Passwords don't match.")
                elif len(password) < 6:
                    st.warning("Password must be at least 6 characters.")
                else:
                    with st.spinner("Creating your account…"):
                        session, message = sign_up(email.strip(), password)
                    if session:
                        persist_session(session)
                        st.session_state.pop("auth_mode", None)
                        st.rerun()
                    elif message:
                        st.info(message)
                        st.session_state.auth_mode = "login"
                    else:
                        st.error("Something went wrong creating your account.")