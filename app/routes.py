import os
from flask import Blueprint, jsonify, redirect, request
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from app.services.spotify_data import (
    get_recently_played,
    get_top_tracks,
    get_top_tracks_last_7_days,
    get_top_artists,
    get_top_artists_last_7_days,
)

api_bp = Blueprint("api", __name__)

# -----------------------------
# Authentication routes
# -----------------------------

def get_auth_manager():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-email user-read-private user-read-recently-played user-top-read",
    )

def get_sp_from_request() -> Spotify | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "): # or len(auth_header.split(" ")) != 2:
        return None
    token = auth_header.split(" ", 1)[1]
    return Spotify(auth=token)

@api_bp.route("/login")
def login():
    auth_url = get_auth_manager().get_authorize_url()
    return redirect(auth_url)

@api_bp.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = get_auth_manager().get_access_token(code)
    access_token = token_info["access_token"]
    return redirect(f"http://localhost:5173?token={access_token}")

# -----------------------------
# Helpers: standard API responses
# -----------------------------

def api_ok(*, data, endpoint: str, period: str | None = None, limit: int | None = None, extra: dict | None = None):
    payload = {
        "ok": True,
        "endpoint": endpoint,
        "count": len(data) if isinstance(data, list) else None,
        "data": data,
    }

    if period is not None:
        payload["period"] = period
    if limit is not None:
        payload["limit"] = limit
    if extra:
        payload.update(extra)

    return jsonify(payload)

def api_err(message: str, status: int = 400, hint=None):
    payload = {
        "ok": False,
        "error": message,
    }
    if hint is not None:
        payload["hint"] = hint
    return jsonify(payload), status


# -----------------------------
# Routes
# -----------------------------

@api_bp.route("/")
def home():
    return (
        "<h1>Spotify Visualizer</h1>"
        "<p>Visit /user, /recent, or /top/tracks/&lt;period&gt;.</p>"
    )


@api_bp.route("/user")
def user_info():
    sp = get_spotify_client()
    me = sp.current_user()

    user_data = {
        "display_name": me.get("display_name"),
        "id": me.get("id"),
        "country": me.get("country"),
        "product": me.get("product"),
    }

    return api_ok(
        data=user_data,
        endpoint="/user",
    )


@api_bp.route("/recent")
def recent_tracks():
    sp = get_sp_from_request()
    if not sp:
        return api_err("Missing or invalid token", status=401) # throws 401 if no token or invalid token provided
    limit = 10
    tracks = get_recently_played(sp, limit=limit) 
    return api_ok(data=tracks, endpoint="/recent", limit=limit)


@api_bp.route("/top/tracks/<period>")
def top_tracks(period: str):
    sp = get_sp_from_request()
    if not sp:
        return api_err("Missing or invalid token", status=401)

    period = period.lower().strip()
    limit = 10

    if period == "week":
        return api_ok(data=get_top_tracks_last_7_days(sp, limit=limit), endpoint="/top/tracks/week", period="week", limit=limit)
    if period == "month":
        return api_ok(data=get_top_tracks(sp, time_range="short_term", limit=limit), endpoint="/top/tracks/month", period="month", limit=limit)
    if period in {"6months", "6m", "halfyear"}:
        return api_ok(data=get_top_tracks(sp, time_range="medium_term", limit=limit), endpoint="/top/tracks/6months", period="6months", limit=limit)
    if period == "year":
        return api_ok(data=get_top_tracks(sp, time_range="long_term", limit=limit), endpoint="/top/tracks/year", period="year", limit=limit)

    return api_err("Invalid period. Use: week, month, 6months, year", status=400, hint=["week", "month", "6months", "year"])   

@api_bp.route("/top/artists/<period>")
def top_artists(period: str):
    sp = get_sp_from_request()
    if not sp:
        return api_err("Missing or invalid token", status=401)

    period = period.lower().strip()
    limit = 10

    if period == "week":
        return api_ok(data=get_top_artists_last_7_days(sp, limit=limit), endpoint="/top/artists/week", period="week", limit=limit)
    if period == "month":
        return api_ok(data=get_top_artists(sp, time_range="short_term", limit=limit), endpoint="/top/artists/month", period="month", limit=limit)
    if period in {"6months", "6m", "halfyear"}:
        return api_ok(data=get_top_artists(sp, time_range="medium_term", limit=limit), endpoint="/top/artists/6months", period="6months", limit=limit)
    if period == "year":
        return api_ok(data=get_top_artists(sp, time_range="long_term", limit=limit), endpoint="/top/artists/year", period="year", limit=limit)

    return api_err("Invalid period. Use: week, month, 6months, year", status=400, hint=["week", "month", "6months", "year"])
