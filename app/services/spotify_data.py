from __future__ import annotations

from datetime import datetime, timedelta, timezone
from collections import Counter
from typing import Any


def get_recently_played(sp, limit: int = 10) -> list[dict[str, Any]]:
    items = sp.current_user_recently_played(limit=limit).get("items", [])
    out = []
    for it in items:
        t = it.get("track") or {}
        out.append({
            "id": t.get("id"),
            "name": t.get("name"),
            "artists": [a.get("name") for a in t.get("artists", [])],
            "album": (t.get("album") or {}).get("name"),
            "image": ((t.get("album") or {}).get("images") or [{}])[0].get("url"),
            "played_at": it.get("played_at"),
            "external_url": (t.get("external_urls") or {}).get("spotify"),
        })
    return out


def get_top_tracks(sp, time_range: str, limit: int = 10) -> list[dict[str, Any]]:
    """
    Spotify-native top tracks:
      - short_term  (~4 weeks)
      - medium_term (~6 months)
      - long_term   (~1-several years)
    """
    items = sp.current_user_top_tracks(time_range=time_range, limit=limit).get("items", [])
    return [
        {
            "id": t.get("id"),
            "name": t.get("name"),
            "artists": [a.get("name") for a in t.get("artists", [])],
            "album": (t.get("album") or {}).get("name"),
            "image": ((t.get("album") or {}).get("images") or [{}])[0].get("url"),
            "popularity": t.get("popularity"),
            "external_url": (t.get("external_urls") or {}).get("spotify"),
        }
        for t in items
    ]


def get_top_tracks_last_7_days(sp, limit: int = 10, recent_limit: int = 50) -> list[dict[str, Any]]:
    """
    Week approximation: count plays from recently played in last 7 days.
    Spotify cap: recently played returns max 50 items.
    """
    recent = sp.current_user_recently_played(limit=recent_limit).get("items", [])
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    played_ids: list[str] = []
    id_to_track: dict[str, dict[str, Any]] = {}

    for item in recent:
        played_at = item.get("played_at")
        track = item.get("track") or {}
        tid = track.get("id")
        if not played_at or not tid:
            continue

        played_dt = datetime.fromisoformat(played_at.replace("Z", "+00:00"))
        if played_dt < cutoff:
            continue

        played_ids.append(tid)
        if tid not in id_to_track:
            id_to_track[tid] = {
                "id": tid,
                "name": track.get("name"),
                "artists": [a.get("name") for a in track.get("artists", [])],
                "album": (track.get("album") or {}).get("name"),
                "image": ((track.get("album") or {}).get("images") or [{}])[0].get("url"),
                "external_url": (track.get("external_urls") or {}).get("spotify"),
            }

    counts = Counter(played_ids)
    ranked = counts.most_common(limit)

    out = []
    for tid, c in ranked:
        row = id_to_track.get(tid, {"id": tid})
        out.append({**row, "plays_last_7_days": c})

    return out


def get_top_artists(sp, time_range: str, limit: int = 10) -> list[dict[str, Any]]:
    """
    Spotify-native top artists:
      - short_term  (~4 weeks)
      - medium_term (~6 months)
      - long_term   (~1-several years)
    """
    items = sp.current_user_top_artists(time_range=time_range, limit=limit).get("items", [])
    return [
        {
            "id": a.get("id"),
            "name": a.get("name"),
            "genres": a.get("genres", []),
            "popularity": a.get("popularity"),
            "followers": (a.get("followers") or {}).get("total"),
            "external_url": (a.get("external_urls") or {}).get("spotify"),
            "images": a.get("images", []),
        }
        for a in items
    ]


def get_top_artists_last_7_days(sp, limit: int = 10, recent_limit: int = 50) -> list[dict[str, Any]]:
    """
    Week approximation: count artist appearances from recently played in last 7 days.
    Spotify cap: recently played returns max 50 items.
    """
    recent = sp.current_user_recently_played(limit=recent_limit).get("items", [])
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    artist_ids: list[str] = []
    id_to_artist: dict[str, dict[str, Any]] = {}

    for item in recent:
        played_at = item.get("played_at")
        track = item.get("track") or {}
        if not played_at:
            continue

        played_dt = datetime.fromisoformat(played_at.replace("Z", "+00:00"))
        if played_dt < cutoff:
            continue

        for artist in track.get("artists", []):
            aid = artist.get("id")
            if not aid:
                continue

            artist_ids.append(aid)
            if aid not in id_to_artist:
                id_to_artist[aid] = {
                    "id": aid,
                    "name": artist.get("name"),
                    "external_url": (artist.get("external_urls") or {}).get("spotify"),
                }

    counts = Counter(artist_ids)
    ranked = counts.most_common(limit)

    out = []
    for aid, c in ranked:
        row = id_to_artist.get(aid, {"id": aid})
        out.append({**row, "plays_last_7_days": c})

    return out