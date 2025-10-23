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

    load_dotenv() # Load environment variables from .env file

    client_id = _require_env("SPOTIPY_CLIENT_ID")
    client_secret = _require_env("SPOTIPY_CLIENT_SECRET")
    redirect_uri = _require_env("SPOTIPY_REDIRECT_URI")
    scopes = os.getenv("SPOTIFY_SCOPES", "user-read-email user-read-private")
    
    auth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scopes,
        open_browser=True, # open the auth URL in the browser
        cache_path=".cache") # cache the token in a file
    
    return spotipy.Spotify(auth_manager=auth)


def get_recently_played(sp, limit: int = 10):
    recent = sp.current_user_recently_played(limit=5)
    tracks = []

    for item in recent.get("items", []):
        track = item.get("track", {})
        artist_names = ", ".join([a.get("name") for a in track.get("artists", [])])
        tracks.append({
            "played_at": item.get("played_at"),
            "name": track.get("name"),
            "artist_name": artist_names, 
            "album": (track.get("album") or {}).get("name"),
            "track_name": track.get("name"),
            })
            
        return tracks

if __name__ == "__main__":
    print("[info] Starting Spotify client test...")

    try:
        sp = _get_spotify_client()  # autenticación + token
        me = sp.current_user()      # llamada de prueba a la API

        print("[ok] Authenticated successfully!\n")
        print(json.dumps({
            "display_name": me.get("display_name"),
            "id": me.get("id"),
            "country": me.get("country"),
            "product": me.get("product")
        }, indent=2))

        for track in get_recently_played(sp, limit=5):
            print(f"- {track['track_name']} by {track['artist_name']}. Played at {track['played_at']})")

    except Exception as e:
        print(f"[error] {type(e).__name__}: {e}")








