from flask import Blueprint, jsonify
from app.services.spotify_client import get_spotify_client
from app.services.spotify_data import (
    get_recently_played,
    get_top_tracks,
    get_top_tracks_last_7_days,
)

api_bp = Blueprint("api", __name__)

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
    sp = get_spotify_client()
    limit = 10
    tracks = get_recently_played(sp, limit=limit)

    return api_ok(
        data=tracks,
        endpoint="/recent",
        limit=limit,
    )


@api_bp.route("/top/tracks/<period>")
def top_tracks(period: str):
    sp = get_spotify_client()
    period = period.lower().strip()
    limit = 10

    if period == "week":
        data = get_top_tracks_last_7_days(sp, limit=limit)
        return api_ok(
            data=data,
            endpoint="/top/tracks/week",
            period="week",
            limit=limit,
        )

    if period == "month":
        data = get_top_tracks(sp, time_range="short_term", limit=limit)
        return api_ok(
            data=data,
            endpoint="/top/tracks/month",
            period="month",
            limit=limit,
        )

    if period in {"6months", "6m", "halfyear"}:
        canonical = "6months"
        data = get_top_tracks(sp, time_range="medium_term", limit=limit)
        return api_ok(
            data=data,
            endpoint="/top/tracks/6months",
            period=canonical,
            limit=limit,
        )

    if period == "year":
        data = get_top_tracks(sp, time_range="long_term", limit=limit)
        return api_ok(
            data=data,
            endpoint="/top/tracks/year",
            period="year",
            limit=limit,
        )

    return api_err(
        "Invalid period. Use: week, month, 6months, year",
        status=400,
        hint=["week", "month", "6months", "year"],
    )
