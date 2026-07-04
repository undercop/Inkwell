"""
Supabase client setup.

Requires SUPABASE_URL and SUPABASE_KEY (the project's anon/public key —
NOT the service_role key) in your .env file. Get both from your Supabase
project: Project Settings -> API.
"""
import os

import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError(
            "Missing SUPABASE_URL / SUPABASE_KEY. Add them to your .env file — "
            "see .env.example."
        )

    return create_client(url, key)
