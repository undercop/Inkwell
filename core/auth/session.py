"""
Keeps the logged-in state in st.session_state, and mirrors just the
refresh token into a browser cookie so that reloading the page doesn't
force the user to log in again.

Note: streamlit-cookies-controller's underlying component needs one
render round-trip to sync cookies to the Python side. In practice this
means on a hard refresh, the very first script run may not see the
cookie yet — ensure_session() handles this by simply doing nothing that
run; the next rerun (triggered by the component itself) picks it up.
"""
from typing import Optional

import streamlit as st
from streamlit_cookies_controller import CookieController

from core.auth.service import AuthSession, restore_session, sign_out as _sign_out

COOKIE_NAME = "inkwell_refresh_token"
COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 30  # 30 days


def _cookie_controller() -> CookieController:
    return CookieController()


def _safe_get(controller: CookieController, name: str):
    """streamlit-cookies-controller's underlying component can be
    momentarily un-synced (its internal cookie dict is None) right after
    a rerun — e.g. immediately following logout. In that state .get()
    raises instead of returning None, so we treat any failure here as
    'no cookie yet' rather than crashing the whole app."""
    try:
        return controller.get(name)
    except Exception:
        return None


def _safe_remove(controller: CookieController, name: str) -> None:
    try:
        controller.remove(name)
    except Exception:
        pass


def _safe_set(controller: CookieController, name: str, value: str, max_age: int) -> None:
    try:
        controller.set(name, value, max_age=max_age)
    except TypeError:
        try:
            controller.set(name, value)
        except Exception:
            pass
    except Exception:
        pass


def ensure_session() -> Optional[AuthSession]:
    """Call once near the top of app.py. Returns the current AuthSession
    (or None if logged out), restoring from the cookie if needed."""
    if "auth_session" not in st.session_state:
        st.session_state.auth_session = None

    if st.session_state.auth_session is None:
        token = _safe_get(_cookie_controller(), COOKIE_NAME)
        if token:
            session = restore_session(token)
            if session:
                st.session_state.auth_session = session

    return st.session_state.auth_session


def persist_session(session: AuthSession) -> None:
    st.session_state.auth_session = session
    _safe_set(_cookie_controller(), COOKIE_NAME, session.refresh_token, COOKIE_MAX_AGE_SECONDS)


def clear_session() -> None:
    _sign_out()
    st.session_state.auth_session = None
    _safe_remove(_cookie_controller(), COOKIE_NAME)
