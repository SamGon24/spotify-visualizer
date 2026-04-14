import os
import logging
from flask import Blueprint, jsonify, redirect, request
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler
from app.services.spotify_data import (
    get_recently_played,
    get_top_tracks,
    get_top_tracks_last_7_days,
    get_top_artists,
    get_top_artists_last_7_days,
)

api_bp = Blueprint("api", __name__)
logger = logging.getLogger(__name__)

# -----------------------------
# Authentication routes
# -----------------------------

def get_auth_manager():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    
    logger.debug(f"🔐 Auth Manager Config - Client ID: {client_id[:10]}..., Redirect URI: {redirect_uri}")
    
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-email user-read-private user-read-recently-played user-top-read",
        cache_handler=MemoryCacheHandler(),
    )

def get_sp_from_request() -> Spotify | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "): # or len(auth_header.split(" ")) != 2:
        logger.warning(f"⚠️  Missing or invalid Authorization header: {auth_header[:20] if auth_header else 'empty'}")
        return None
    token = auth_header.split(" ", 1)[1]
    logger.debug(f"✅ Valid Bearer token found")
    return Spotify(auth=token)

@api_bp.route("/login")
def login():
    logger.info("🔑 /login endpoint called")
    try:
        auth_url = get_auth_manager().get_authorize_url()
        logger.info(f"✅ Authorization URL generated: {auth_url[:50]}...")
        return redirect(auth_url)
    except Exception as e:
        logger.error(f"❌ Error in /login: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route("/callback")
def callback():
    logger.info("🔄 /callback endpoint called")
    try:
        code = request.args.get("code")
        logger.info(f"📝 Authorization code received: {code[:20] if code else 'None'}...")
        
        if not code:
            logger.error("❌ No authorization code in callback")
            return jsonify({"error": "No code provided"}), 400
        
        token_info = get_auth_manager().get_access_token(code)
        access_token = token_info["access_token"]
        refresh_token = token_info.get("refresh_token", "")
        expires_in = token_info.get("expires_in", 3600)
        logger.info(f"✅ Access token obtained: {access_token[:20]}...")

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        redirect_url = f"{frontend_url}?token={access_token}&refresh={refresh_token}&expires_in={expires_in}"
        logger.info(f"🔀 Redirecting to: {redirect_url[:50]}...")
        return redirect(redirect_url)
    except Exception as e:
        logger.error(f"❌ Error in /callback: {str(e)}")
        return jsonify({"error": str(e)}), 500

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

@api_bp.route("/refresh")
def refresh_token():
    logger.info("🔄 /refresh endpoint called")
    refresh_token = request.args.get("refresh_token")
    if not refresh_token:
        return api_err("Missing refresh_token parameter", status=400)
    try:
        token_info = get_auth_manager().refresh_access_token(refresh_token)
        return jsonify({
            "ok": True,
            "access_token": token_info["access_token"],
            "expires_in": token_info.get("expires_in", 3600),
        })
    except Exception as e:
        logger.error(f"❌ /refresh: {str(e)}")
        return api_err("Failed to refresh token", status=401)


@api_bp.route("/")
def home():
    return (
        "<h1>Spotify Visualizer</h1>"
        "<p>Visit /user, /recent, or /top/tracks/&lt;period&gt;.</p>"
    )


@api_bp.route("/user")
def user_info():
    logger.info("👤 /user endpoint called")
    sp = get_sp_from_request()
    if not sp:
        logger.warning("❌ /user: No valid token provided")
        return api_err("Missing or invalid token", status=401)
    
    try:
        me = sp.current_user()
        logger.info(f"✅ /user: User info retrieved: {me.get('display_name')}")

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
    except Exception as e:
        logger.error(f"❌ /user: Error retrieving user info: {str(e)}")
        return api_err(f"Error retrieving user info: {str(e)}", status=500)


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
