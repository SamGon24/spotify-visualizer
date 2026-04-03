# Spotify Visualizer - Architecture & UML Documentation

## Project Overview
This is a Flask-based web application that connects to the Spotify API to retrieve and visualize user listening data including recently played tracks, top tracks, and top artists across various time periods.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         External Services                               │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │              Spotify Web API (spotipy library)                 │   │
│  │  • Authentication (OAuth 2.0)                                  │   │
│  │  • Current User Info                                           │   │
│  │  • Recently Played                                             │   │
│  │  • Top Tracks (by time range)                                  │   │
│  │  • Top Artists (by time range)                                 │   │
│  └─────────────────┬──────────────────────────────────────────────┘   │
└────────────────────┼────────────────────────────────────────────────────┘
                     │
                     │ Uses
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Flask Web Application                                │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     app/__init__.py                              │  │
│  │  create_app() → Flask                                            │  │
│  │  • Initializes Flask app                                         │  │
│  │  • Registers blueprints                                          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    app/routes.py (Blueprint)                     │  │
│  │  Defines REST API endpoints:                                     │  │
│  │  • GET /                           → home()                      │  │
│  │  • GET /user                       → user_info()                 │  │
│  │  • GET /recent                     → recent_tracks()             │  │
│  │  • GET /top/tracks/<period>        → top_tracks()                │  │
│  │  • GET /top/artists/<period>       → top_artists()               │  │
│  │                                                                   │  │
│  │  Helper Functions:                                               │  │
│  │  • api_ok()      → Standard success response                     │  │
│  │  • api_err()     → Standard error response                       │  │
│  └─────────────────┬────────────────────────────────────────────────┘  │
│                    │                                                    │
│                    │ Uses                                               │
│                    ▼                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                   Services Layer                                 │  │
│  │                                                                   │  │
│  │  ┌────────────────────────────────────────────────────────────┐ │  │
│  │  │  app/services/spotify_client.py                            │ │  │
│  │  │  • get_spotify_client() → SpotifyOAuth client              │ │  │
│  │  │    - Loads environment variables                           │ │  │
│  │  │    - Sets up OAuth authentication                          │ │  │
│  │  │    - Manages cache                                         │ │  │
│  │  └────────────────────────────────────────────────────────────┘ │  │
│  │                                                                   │  │
│  │  ┌────────────────────────────────────────────────────────────┐ │  │
│  │  │  app/services/spotify_data.py                              │ │  │
│  │  │  Data extraction & transformation functions:               │ │  │
│  │  │  • get_recently_played()      → List[Track]                │ │  │
│  │  │  • get_top_tracks()           → List[Track]                │ │  │
│  │  │  • get_top_tracks_last_7_days() → List[Track] (weighted)   │ │  │
│  │  │  • get_top_artists()          → List[Artist]               │ │  │
│  │  │  • get_top_artists_last_7_days() → List[Artist] (weighted) │ │  │
│  │  └────────────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                      Standalone Utilities                               │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      retrieve.py                                 │  │
│  │  Standalone script for data retrieval & CSV export              │  │
│  │  • _get_spotify_client()  → Spotify auth                        │  │
│  │  • get_recently_played()  → Extract tracks                      │  │
│  │  • save_recent_tracks()   → Export to CSV                       │  │
│  │                                                                   │  │
│  │  Main execution:                                                │  │
│  │  1. Authenticate with Spotify                                   │  │
│  │  2. Fetch recently played tracks                                │  │
│  │  3. Save to recent_tracks.csv                                   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        Entry Point                                      │
│  app/__main__.py                                                        │
│  • create_app() → Flask app                                             │
│  • app.run(debug=True)                                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Class & Function Diagram

### spotify_client.py
```
┌─────────────────────────────────────────────┐
│         spotify_client Module               │
├─────────────────────────────────────────────┤
│ Functions:                                  │
│                                             │
│ get_spotify_client()                        │
│   ├─ Imports: spotipy, SpotifyOAuth        │
│   ├─ Loads: .env → (CLIENT_ID,             │
│   │            SECRET, REDIRECT_URI)       │
│   ├─ Scope: "user-top-read                 │
│   │         user-read-recently-played"     │
│   └─ Returns: spotipy.Spotify (client)     │
│                                             │
│ _require_env(var: str) → str               │
│   └─ Raises EnvironmentError if missing    │
└─────────────────────────────────────────────┘
```

### spotify_data.py
```
┌──────────────────────────────────────────────────────────────────┐
│                    spotify_data Module                           │
├──────────────────────────────────────────────────────────────────┤
│ Type: List[dict[str, Any]]                                       │
│                                                                  │
│ Track Object:                                                    │
│ {                                                                │
│   "id": str,                                                     │
│   "name": str,                                                   │
│   "artists": List[str],                                          │
│   "album": str | None,                                           │
│   "played_at": str (ISO format) | None,                          │
│   "popularity": int | None,                                      │
│   "external_url": str | None,                                    │
│   "plays_last_7_days": int (optional)                            │
│ }                                                                │
│                                                                  │
│ Artist Object:                                                   │
│ {                                                                │
│   "id": str,                                                     │
│   "name": str,                                                   │
│   "genres": List[str],                                           │
│   "popularity": int | None,                                      │
│   "followers": int | None,                                       │
│   "external_url": str | None,                                    │
│   "images": List[dict] | None,                                   │
│   "plays_last_7_days": int (optional)                            │
│ }                                                                │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ Functions:                                                       │
│                                                                  │
│ get_recently_played(sp, limit=10)                                │
│   ├─ Calls: sp.current_user_recently_played()                   │
│   ├─ Extracts: Track metadata + played_at timestamp             │
│   └─ Returns: List[Track] sorted by play date DESC              │
│                                                                  │
│ get_top_tracks(sp, time_range, limit=10)                        │
│   ├─ time_range ∈ {"short_term", "medium_term", "long_term"}   │
│   ├─ Calls: sp.current_user_top_tracks()                        │
│   ├─ Extracts: Track + popularity                               │
│   └─ Returns: List[Track]                                       │
│                                                                  │
│ get_top_tracks_last_7_days(sp, limit=10, recent_limit=50)       │
│   ├─ Calls: sp.current_user_recently_played(limit=50)           │
│   ├─ Filters: items played_at ≥ (now - 7 days)                  │
│   ├─ Counts: track occurrences (plays_last_7_days)              │
│   ├─ Uses: Counter from collections                             │
│   └─ Returns: Top limit tracks by play count                    │
│                                                                  │
│ get_top_artists(sp, time_range, limit=10)                       │
│   ├─ time_range ∈ {"short_term", "medium_term", "long_term"}   │
│   ├─ Calls: sp.current_user_top_artists()                       │
│   ├─ Extracts: Artist metadata                                  │
│   └─ Returns: List[Artist]                                      │
│                                                                  │
│ get_top_artists_last_7_days(sp, limit=10, recent_limit=50)      │
│   ├─ Calls: sp.current_user_recently_played(limit=50)           │
│   ├─ Filters: items played_at ≥ (now - 7 days)                  │
│   ├─ Counts: artist appearances (plays_last_7_days)             │
│   ├─ Uses: Counter from collections                             │
│   └─ Returns: Top limit artists by appearance count             │
└──────────────────────────────────────────────────────────────────┘
```

### routes.py (Blueprint)
```
┌──────────────────────────────────────────────────────────────────┐
│                      routes Module                               │
├──────────────────────────────────────────────────────────────────┤
│ Blueprint: api_bp ("/")                                          │
│                                                                  │
├──────────── Helper Functions ────────────────────────────────────┤
│                                                                  │
│ api_ok(data, endpoint, period?, limit?, extra?)                 │
│   └─ Returns: JSON response                                     │
│      {                                                           │
│        "ok": True,                                               │
│        "endpoint": str,                                          │
│        "count": int | None,                                      │
│        "data": List | dict,                                      │
│        "period"?: str,                                           │
│        "limit"?: int,                                            │
│        ...(extra)                                                │
│      }                                                           │
│                                                                  │
│ api_err(message, status?, hint?)                                │
│   └─ Returns: JSON response (tuple with status code)            │
│      {                                                           │
│        "ok": False,                                              │
│        "error": str,                                             │
│        "hint"?: str | List                                       │
│      }                                                           │
│                                                                  │
├──────────── Endpoints ────────────────────────────────────────────┤
│                                                                  │
│ GET / → home()                                                   │
│   └─ HTML response with navigation links                        │
│                                                                  │
│ GET /user → user_info()                                          │
│   ├─ Gets: current user profile                                 │
│   ├─ Extracts: display_name, id, country, product              │
│   └─ Returns: api_ok(data=user_data, endpoint="/user")          │
│                                                                  │
│ GET /recent → recent_tracks()                                    │
│   ├─ Calls: get_recently_played(sp, limit=10)                  │
│   └─ Returns: api_ok(data=tracks, endpoint="/recent", limit=10) │
│                                                                  │
│ GET /top/tracks/<period> → top_tracks(period)                   │
│   ├─ period ∈ {"week", "month", "6months", "year"}             │
│   ├─ week      → get_top_tracks_last_7_days()                  │
│   ├─ month     → get_top_tracks(time_range="short_term")       │
│   ├─ 6months   → get_top_tracks(time_range="medium_term")      │
│   ├─ year      → get_top_tracks(time_range="long_term")        │
│   └─ Default: api_err("Invalid period...", status=400)         │
│                                                                  │
│ GET /top/artists/<period> → top_artists(period)                 │
│   ├─ period ∈ {"week", "month", "6months", "year"}             │
│   ├─ week      → get_top_artists_last_7_days()                 │
│   ├─ month     → get_top_artists(time_range="short_term")      │
│   ├─ 6months   → get_top_artists(time_range="medium_term")     │
│   ├─ year      → get_top_artists(time_range="long_term")       │
│   └─ Default: api_err("Invalid period...", status=400)         │
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Request → Response Flow
```
┌─────────────┐
│HTTP Request │
│GET /endpoint│
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Flask Router                          │
│ @api_bp.route("/endpoint")            │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Route Handler Function                │
│ e.g., user_info(), recent_tracks()   │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ get_spotify_client()                  │
│ Returns authenticated Spotify client   │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Spotify Data Function                 │
│ e.g., get_recently_played(sp, limit)  │
│                                        │
│ 1. Calls Spotify API via spotipy       │
│ 2. Parses response                     │
│ 3. Transforms data                     │
│ 4. Returns List[dict]                  │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Response Helper                       │
│ api_ok(data, endpoint, ...)           │
│ Formats as JSON                       │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Flask jsonify()                       │
│ Sends HTTP Response (JSON)            │
└──────┬───────────────────────────────┘
       │
       ▼
┌─────────────┐
│HTTP Response│
│  JSON Body  │
└─────────────┘
```

---

## Time Range Mapping

```
┌─────────────────────────────────────────────────────────────────┐
│  API Period         Spotify time_range    Function Used          │
├─────────────────────────────────────────────────────────────────┤
│  /top/*/week        N/A (custom)          *_last_7_days()        │
│  /top/*/month       short_term (~4w)      *(..., "short_term")   │
│  /top/*/6months     medium_term (~6m)     *(..., "medium_term")  │
│  /top/*/year        long_term (~1y+)      *(..., "long_term")    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Dependencies & Environment Variables

### Requirements (from requirements.txt)
```
spotipy==2.24.0          # Spotify API client
python-dotenv==1.0.1     # .env file loader
pandas==2.14.0           # Data manipulation
numpy==1.26.4            # Numerical computing
matplotlib==3.9.2        # Plotting
seaborn==0.12.3          # Statistical visualization
flask==3.0.3             # Web framework
flask-cors==4.1.2        # CORS support
requests==2.31.0         # HTTP requests
```

### Environment Variables (OAuth)
```
SPOTIPY_CLIENT_ID       # Required: Spotify app ID
SPOTIPY_CLIENT_SECRET   # Required: Spotify app secret
SPOTIPY_REDIRECT_URI    # Required: OAuth callback URL
SPOTIFY_SCOPES          # Optional: OAuth scopes (default set in code)
```

### Cache Files
```
.spotify_cache           # OAuth token cache (retrieve.py)
.spotify_cache           # OAuth token cache (spotify_client.py)
recent_tracks.csv        # Output file (retrieve.py)
```

---

## Potential Improvements & Issues

### 1. **Code Duplication**
- `spotify_client.py` and `retrieve.py` both define Spotify client initialization
- **Suggestion**: Share common logic, use `app.services.spotify_client` in `retrieve.py`

### 2. **Weak Separation of Concerns**
- Route handlers directly call data functions
- **Suggestion**: Create a service/business logic layer between routes and data functions

### 3. **Limited Error Handling**
- Missing try-catch blocks around API calls
- **Suggestion**: Add exception handling for network failures, API rate limits, auth errors

### 4. **No Caching Strategy**
- Every API request hits Spotify (could hit rate limits)
- **Suggestion**: Implement response caching with TTL

### 5. **Hard-coded Limits & Defaults**
- `limit=10` scattered throughout
- **Suggestion**: Centralize configuration in config file or constants module

### 6. **Testing & Logging**
- No unit tests
- No structured logging
- **Suggestion**: Add pytest tests and logging setup

### 7. **Frontend Missing**
- API endpoints exist but no UI to visualize data
- **Suggestion**: Build React/Vue frontend or add matplotlib visualization endpoints

### 8. **Missing Documentation**
- No API documentation (Swagger/OpenAPI)
- **Suggestion**: Use Flask-RESTX or add Swagger decorators

---

## Tech Stack Summary
| Layer | Technology |
|-------|-----------|
| **API Client** | Spotipy 2.24.0 |
| **Web Framework** | Flask 3.0.3 |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Configuration** | python-dotenv |
| **HTTP/CORS** | Requests, Flask-CORS |
