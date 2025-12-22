from __future__ import annotations

import os
import sys
import json
import pandas as pd
from dotenv import load_dotenv


def _require_env(var: str) -> str:
    value = os.getenv(var)
    if not value:
        raise EnvironmentError(f"Required environment variable '{var}' not found.")
    return value


def _get_spotify_client():
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth
    except ImportError:
        print(
            "The 'spotipy' library is required. Install it with: pip install spotipy",
            file=sys.stderr
        )
        raise

    load_dotenv()

    client_id = _require_env("SPOTIPY_CLIENT_ID")
    client_secret = _require_env("SPOTIPY_CLIENT_SECRET")
    redirect_uri = _require_env("SPOTIPY_REDIRECT_URI")

    scopes = os.getenv(
        "SPOTIFY_SCOPES",
        "user-read-email user-read-private user-read-recently-played"
    )

    auth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scopes,
        open_browser=True,
        cache_path=".cache"
    )

    return spotipy.Spotify(auth_manager=auth)


def get_recently_played(sp, limit: int = 20):
    recent = sp.current_user_recently_played(limit=limit)
    tracks = []

    for item in recent.get("items", []):
        track = item.get("track", {}) or {}
        album = track.get("album") or {}
        artists = track.get("artists") or []
        artist_names = ", ".join([a.get("name", "") for a in artists if a.get("name")])

        tracks.append({
            "played_at": item.get("played_at"),
            "track_name": track.get("name"),
            "artist_name": artist_names,
            "album_name": album.get("name"),
            "track_id": track.get("id"),
        })

    return tracks


def save_recent_tracks(tracks, filename: str = "recent_tracks.csv"):
    df = pd.DataFrame(tracks)

    # optional: normalize played_at to datetime
    if "played_at" in df.columns:
        df["played_at"] = pd.to_datetime(df["played_at"], errors="coerce", utc=True)

    df.to_csv(filename, index=False)
    return df


if __name__ == "__main__":
    print("[info] Starting Spotify client test...")

    try:
        sp = _get_spotify_client()
        me = sp.current_user()

        print("[ok] Authenticated successfully!\n")
        print(json.dumps({
            "display_name": me.get("display_name"),
            "id": me.get("id"),
            "country": me.get("country"),
            "product": me.get("product"),
        }, indent=2))

        tracks = get_recently_played(sp, limit=10)
        df = save_recent_tracks(tracks, "recent_tracks.csv")

        print("\n[ok] Saved recent_tracks.csv")
        for i, t in enumerate(tracks[:5], start=1):
            print(f"{i}. {t['track_name']} — {t['artist_name']} ({t['played_at']})")

    except Exception as e:
        print(f"[error] {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)







