from flask import Blueprint, jsonify
from retrieve import _get_spotify_client, get_recently_played

api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def home():
    return "<h1>Spotify Visualizer</h1><p>Visit /user or /recent to test the API.</p>"

@api_bp.route("/user")
def user_info():
    sp = _get_spotify_client()
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
    sp = _get_spotify_client()
    tracks = get_recently_played(sp, limit=10)
    return jsonify(tracks)
