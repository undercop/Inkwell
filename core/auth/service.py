"""
UI-free wrappers around Supabase Auth calls. Keeping these separate from
core/auth/ui.py means the actual network/auth logic can be tested or
swapped out without touching any Streamlit code.
"""
from dataclasses import dataclass
from typing import Optional

from core.auth.supabase_client import get_supabase_client


@dataclass
class AuthSession:
    access_token: str
    refresh_token: str
    user_id: str
    email: str


def _session_from_response(response) -> Optional[AuthSession]:
    session = getattr(response, "session", None)
    user = getattr(response, "user", None)
    if not session or not user:
        return None
    return AuthSession(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        user_id=user.id,
        email=user.email or "",
    )


def sign_up(email: str, password: str) -> tuple[Optional[AuthSession], Optional[str]]:
    """Returns (session, message). session is None if email confirmation
    is required by the Supabase project's auth settings — in that case
    message explains what to do next."""
    client = get_supabase_client()
    try:
        response = client.auth.sign_up({"email": email, "password": password})
    except Exception as e:
        return None, _friendly_error(e)

    session = _session_from_response(response)
    if session:
        return session, None

    return None, (
        "Account created. Check your email to confirm it, then log in — "
        "your Supabase project has email confirmation enabled."
    )


def sign_in(email: str, password: str) -> tuple[Optional[AuthSession], Optional[str]]:
    client = get_supabase_client()
    try:
        response = client.auth.sign_in_with_password({"email": email, "password": password})
    except Exception as e:
        return None, _friendly_error(e)

    session = _session_from_response(response)
    if session:
        return session, None
    return None, "Login failed — please check your email and password."


def sign_out() -> None:
    client = get_supabase_client()
    try:
        client.auth.sign_out()
    except Exception:
        pass  # best-effort; local session state gets cleared regardless


def restore_session(refresh_token: str) -> Optional[AuthSession]:
    """Used to silently re-authenticate from a saved refresh token
    (e.g. read from a browser cookie) after a page refresh."""
    client = get_supabase_client()
    try:
        response = client.auth.refresh_session(refresh_token)
    except Exception:
        return None
    return _session_from_response(response)


def _friendly_error(e: Exception) -> str:
    msg = str(e)
    if "already registered" in msg.lower() or "already exists" in msg.lower():
        return "An account with that email already exists — try logging in instead."
    if "invalid login credentials" in msg.lower():
        return "Incorrect email or password."
    if "password" in msg.lower() and ("least" in msg.lower() or "short" in msg.lower()):
        return "Password is too short — Supabase requires at least 6 characters."
    return msg
