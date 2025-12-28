from flask import Blueprint, jsonify
from app.services.spotify_client import get_spotify_client
from app.services.spotify_data import (
    get_recently_played,
    get_top_tracks,
    get_top_tracks_last_7_days,
)

api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def home():
    return "<h1>Spotify Visualizer</h1><p>Visit /user, /recent, or /top/tracks/&lt;period&gt;.</p>"

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
    return jsonify(user_data)

@api_bp.route("/recent")
def recent_tracks():
    sp = get_spotify_client()
    tracks = get_recently_played(sp, limit=10)
    return jsonify(tracks)

@api_bp.route("/top/tracks/<period>")
def top_tracks(period: str):
    sp = get_spotify_client()
    period = period.lower().strip()
    limit = 10

    if period == "week":
        # Aproximación: últimos 7 días usando recently played (Spotify cap: 50 items)
        return jsonify(get_top_tracks_last_7_days(sp, limit=limit))

    if period == "month":
        # ~4 weeks
        return jsonify(get_top_tracks(sp, time_range="short_term", limit=limit))

    if period in {"6months", "6m", "halfyear"}:
        # ~6 months
        return jsonify(get_top_tracks(sp, time_range="medium_term", limit=limit))

    if period == "year":
        # Spotify no da "1 año exacto"; long_term es lo más cercano
        return jsonify(get_top_tracks(sp, time_range="long_term", limit=limit))

    return jsonify({"error": "Invalid period. Use: week, month, 6months, year"}), 400
