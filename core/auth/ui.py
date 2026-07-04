import streamlit as st

from core.auth.service import sign_up, sign_in
from core.auth.session import persist_session
from core.ui.theme import inject_base_styles, APP_NAME, APP_TAGLINE, BRAND, BOOKS, BLOG


def _hide_app_chrome() -> None:
    """This page has no sidebar / nav — hide the (otherwise empty) sidebar
    and its collapse arrow so it reads as a distinct, standalone screen."""
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] { display: none; }
        [data-testid="collapsedControl"] { display: none; }
        .block-container { padding-top: 0 !important; max-width: 100% !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _auth_page_styles() -> None:
    st.markdown(
        f"""
        <style>
        .auth-shell {{
            min-height: 100vh;
            display: flex;
        }}
        .auth-brand-panel {{
            background: linear-gradient(160deg, #171a24 0%, #0b0d13 70%);
            border-right: 1px solid rgba(255,255,255,0.08);
            padding: 3rem 2.8rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100%;
            min-height: 560px;
            border-radius: 22px;
        }}
        .auth-brand-panel .brand-mark {{
            font-family: 'Fraunces', serif;
            font-size: 2.1rem;
            font-weight: 700;
            color: #f5f6fb;
            margin-bottom: 0.4rem;
        }}
        .auth-brand-panel .brand-mark .dot {{ color: {BRAND}; }}
        .auth-brand-panel .brand-sub {{
            color: #9b9fc2;
            font-size: 1rem;
            max-width: 320px;
            line-height: 1.6;
            margin-bottom: 2rem;
        }}
        .auth-shelf {{
            display: flex;
            align-items: flex-end;
            gap: 6px;
            height: 70px;
        }}
        .auth-shelf .spine {{ width: 14px; border-radius: 3px 3px 0 0; opacity: 0.85; }}

        .auth-card {{
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 22px;
            padding: 2.6rem 2.6rem 2rem 2.6rem;
            max-width: 400px;
            margin: 0 auto;
        }}
        .auth-card h2 {{
            font-family: 'Fraunces', serif;
            font-size: 1.6rem;
            margin-bottom: 0.3rem;
            color: #f2f3fa;
        }}
        .auth-card p.sub {{
            color: #9b9fc2;
            font-size: 0.92rem;
            margin-bottom: 1.6rem;
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

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"
    mode = st.session_state.auth_mode

    st.markdown("<div style='height: 4vh;'></div>", unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(
            f"""
            <div class="auth-brand-panel">
                <div class="brand-mark">🖋️ {APP_NAME}<span class="dot">.</span></div>
                <div class="brand-sub">{APP_TAGLINE} — sign in to find your next
                read or draft your next post.</div>
                <div class="auth-shelf">
                    <div class="spine" style="height:44px; background:{BOOKS};"></div>
                    <div class="spine" style="height:60px; background:{BLOG};"></div>
                    <div class="spine" style="height:34px; background:{BOOKS};"></div>
                    <div class="spine" style="height:52px; background:{BOOKS};"></div>
                    <div class="spine" style="height:40px; background:{BLOG};"></div>
                    <div class="spine" style="height:64px; background:{BOOKS};"></div>
                    <div class="spine" style="height:30px; background:{BLOG};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        if mode == "login":
            st.markdown("<h2>Welcome back</h2>", unsafe_allow_html=True)
            st.markdown("<p class='sub'>Log in to continue.</p>", unsafe_allow_html=True)
        else:
            st.markdown("<h2>Create your account</h2>", unsafe_allow_html=True)
            st.markdown("<p class='sub'>Takes less than a minute.</p>", unsafe_allow_html=True)

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

        st.markdown("</div>", unsafe_allow_html=True)
