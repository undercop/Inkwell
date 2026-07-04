"""
Thin wrapper around streamlit-authenticator.

Keeps two concerns out of app.py:
  1. Reading/writing config/auth_config.yaml (credentials, cookie settings).
  2. Constructing the Authenticate object from it.

We deliberately don't cache build_authenticator() with st.cache_resource —
registering a new user or resetting a password mutates the credentials
dict and must be saved back to disk, so we want a fresh read each rerun.
It's just one small YAML file, so this is cheap.
"""
from pathlib import Path
from typing import Any, Dict

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "auth_config.yaml"

_DEFAULT_CONFIG: Dict[str, Any] = {
    "credentials": {"usernames": {}},
    "cookie": {
        "name": "inkwell_auth",
        "key": "change-this-to-a-long-random-string",
        "expiry_days": 30,
    },
    "preauthorized": {"emails": []},
}


def load_config() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        save_config(_DEFAULT_CONFIG)
        return yaml.safe_load(yaml.dump(_DEFAULT_CONFIG))  # deep copy

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=SafeLoader)

    # Guard against a hand-edited file missing a section.
    config.setdefault("credentials", {"usernames": {}})
    config["credentials"].setdefault("usernames", {})
    config.setdefault("cookie", _DEFAULT_CONFIG["cookie"])
    config.setdefault("preauthorized", {"emails": []})
    return config


def save_config(config: Dict[str, Any]) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False)


def build_authenticator():
    """Returns (authenticator, config). Call save_config(config) after any
    widget that mutates credentials (register_user, reset_password, etc.)."""
    config = load_config()
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        auto_hash=True,  # hashes plain-text passwords found in the config automatically
    )
    return authenticator, config
