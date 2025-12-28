from __future__ import annotations
import os
import sys
from dotenv import load_dotenv

def _require_env(var: str) -> str:
    value = os.getenv(var)
    if not value:
        raise EnvironmentError(f"Required environment variable '{var}' not found.")
    return value

def get_spotify_client():
    """
    Centralized Spotify client creation.
    """
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth
    except ImportError:
        raise ImportError(
            "The 'spotipy' library is required. Install it via: pip install spotipy",
            file=sys.stderr,
        )

    load_dotenv()

    client_id = _require_env("SPOTIPY_CLIENT_ID")
    client_secret = _require_env("SPOTIPY_CLIENT_SECRET")
    redirect_uri = _require_env("SPOTIPY_REDIRECT_URI")

    scope = "user-top-read user-read-recently-played"

    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            cache_path=".spotify_cache",
        )
    )
