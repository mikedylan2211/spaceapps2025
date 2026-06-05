import os
from functools import lru_cache

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


TOKEN_URL = (
    "https://services.sentinel-hub.com/auth/realms/main/protocol/"
    "openid-connect/token"
)


def _streamlit_secret(*keys):
    try:
        import streamlit as st

        value = st.secrets
        for key in keys:
            value = value[key]
        return value
    except Exception:
        return None


def _config_value(env_name, *secret_paths):
    env_value = os.getenv(env_name)
    if env_value:
        return env_value

    for path in secret_paths:
        value = _streamlit_secret(*path)
        if value:
            return value

    return None


def get_sentinel_credentials():
    client_id = _config_value(
        "SENTINEL_CLIENT_ID",
        ("sentinel_hub", "client_id"),
        ("SENTINEL_CLIENT_ID",),
    )
    client_secret = _config_value(
        "SENTINEL_CLIENT_SECRET",
        ("sentinel_hub", "client_secret"),
        ("SENTINEL_CLIENT_SECRET",),
    )
    return client_id, client_secret


@lru_cache(maxsize=1)
def _fetch_token(client_id, client_secret):
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(
        token_url=TOKEN_URL,
        client_secret=client_secret,
        include_client_id=True,
    )
    return token["access_token"]


def make_token():
    client_id, client_secret = get_sentinel_credentials()
    if not client_id or not client_secret:
        raise RuntimeError(
            "Missing Sentinel Hub credentials. Set SENTINEL_CLIENT_ID and "
            "SENTINEL_CLIENT_SECRET, or add them to .streamlit/secrets.toml."
        )

    return _fetch_token(client_id, client_secret)
