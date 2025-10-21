# This file is the first step in the data pipeline.
# It retrieves the user's recently played tracks from the Spotify API
# and saves the data to a CSV file for further processing.

from __future__ import annotations
import os
import pandas as pd
import json
import sys

from dotenv import load_dotenv

def _require_env(var: str) -> str:
    value = os.getenv(var)
    if value is None:
        raise EnvironmentError(f"Required environment variable '{var}' not found.")
    return value

def _get_spotify_client():
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth
    except ImportError:
        raise ImportError("The 'spotipy' library is required to run this script. Please install it via 'pip install spotipy'.",
                          file=sys.stderr)

    # justto check everything is working (dependencies)


