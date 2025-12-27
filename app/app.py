# app.py
import os, sys
sys.path.append(os.path.dirname(__file__))  # fuerza a Python a usar tu retrieve.py local

from flask import Flask, jsonify
from retrieve import _get_spotify_client, get_recently_played

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Spotify Visualizer</h1><p>Visit /user or /recent to test the API.</p>"

@app.route("/user")
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

@app.route("/recent")
def recent_tracks():
    sp = _get_spotify_client()
    tracks = get_recently_played(sp, limit=10)
    return jsonify(tracks)

if __name__ == "__main__":
    app.run(debug=True)
