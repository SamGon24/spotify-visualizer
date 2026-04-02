# Spotify Visualizer - Setup & Execution Guide

## Prerequisites
- Python 3.9+ (check with `python3 --version`)
- Spotify account (free or premium)
- Spotify Developer account (to create an app)

---

## Step 1: Create Spotify App & Get Credentials

### 1.1 Go to Spotify Developer Dashboard
1. Visit: https://developer.spotify.com/dashboard
2. Log in with your Spotify account (or create one)
3. Accept terms and create an account

### 1.2 Create an Application
1. Click **"Create an App"**
2. Enter an app name (e.g., "Spotify Visualizer")
3. Accept the terms and create
4. Accept again if asked for developer terms

### 1.3 Get Your Credentials
On your app's dashboard, you'll see:
- **Client ID** ← Copy this
- **Client Secret** ← Copy this (keep it secret!)

### 1.4 Set Redirect URI
1. Click **"Edit Settings"**
2. Add a **Redirect URI** (e.g., `http://localhost:8888/callback`)
3. Save

---

## Step 2: Clone & Setup Project

### 2.1 Clone the Repository (if not already done)
```bash
git clone https://github.com/SamGon24/Spotify-Visualizer.git
cd Spotify-Visualizer/spotify-visualizer
```

### 2.2 Create Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# On Windows: venv\Scripts\activate
```

### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Step 3: Configure Environment Variables

### 3.1 Create `.env` File
```bash
# In the project root directory, create a .env file
touch .env
```

### 3.2 Add Your Spotify Credentials
Edit `.env` and add:
```env
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

⚠️ **Important**: 
- Replace `your_client_id_here` with your actual Client ID
- Replace `your_client_secret_here` with your actual Client Secret
- Never commit `.env` to git (it's already in `.gitignore`)

---

## Step 4: Run the Project

### Option A: Run the Web API (Recommended)

```bash
# Make sure your virtual environment is activated
# source venv/bin/activate

# Run the Flask app
python3 -m app
```

Output should show:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

**Test the API:**
- Home page: http://localhost:5000/
- User info: http://localhost:5000/user
- Recent tracks: http://localhost:5000/recent
- Top tracks (week): http://localhost:5000/top/tracks/week
- Top tracks (month): http://localhost:5000/top/tracks/month
- Top tracks (6months): http://localhost:5000/top/tracks/6months
- Top tracks (year): http://localhost:5000/top/tracks/year
- Top artists (week): http://localhost:5000/top/artists/week
- Top artists (month): http://localhost:5000/top/artists/month
- Top artists (6months): http://localhost:5000/top/artists/6months
- Top artists (year): http://localhost:5000/top/artists/year

### Option B: Run One-Time Data Retrieval Script

```bash
# This retrieves recently played tracks and saves to CSV
python3 retrieve.py
```

Output:
```
[info] Starting Spotify client test...
[ok] Authenticated successfully!

{
  "display_name": "Your Name",
  "id": "your_spotify_id",
  "country": "US",
  "product": "premium"
}

[ok] Saved recent_tracks.csv
1. Song Name — Artist Name (2026-03-31T12:00:00Z)
2. Another Song — Another Artist (2026-03-31T11:30:00Z)
...
```

---

## Step 5: First-Time Authentication

### When You First Run the App
1. A browser window will open automatically
2. Click **"Agree"** to authorize the app
3. You'll be redirected to `http://localhost:8888/callback`
4. The app caches your token in `.spotify_cache` (don't delete!)

### If You Get Auth Errors
- Delete `.spotify_cache` file
- Delete `.spotify_cache-<username>` if it exists
- Run the app again to re-authenticate

---

## API Response Examples

### GET /user
```json
{
  "ok": true,
  "endpoint": "/user",
  "count": null,
  "data": {
    "display_name": "Your Name",
    "id": "spotify_user_id",
    "country": "US",
    "product": "premium"
  }
}
```

### GET /recent
```json
{
  "ok": true,
  "endpoint": "/recent",
  "count": 10,
  "limit": 10,
  "data": [
    {
      "id": "track_id",
      "name": "Song Name",
      "artists": ["Artist 1", "Artist 2"],
      "album": "Album Name",
      "played_at": "2026-03-31T12:00:00Z",
      "external_url": "https://open.spotify.com/track/..."
    },
    ...
  ]
}
```

### GET /top/tracks/week
```json
{
  "ok": true,
  "endpoint": "/top/tracks/week",
  "count": 10,
  "period": "week",
  "limit": 10,
  "data": [
    {
      "id": "track_id",
      "name": "Most Played Song",
      "artists": ["Artist"],
      "album": "Album",
      "popularity": 85,
      "external_url": "https://...",
      "plays_last_7_days": 5
    },
    ...
  ]
}
```

---

## Troubleshooting

### Issue: "Required environment variable 'SPOTIPY_CLIENT_ID' not found"
**Solution**: 
- Make sure `.env` file exists in the project root
- Verify you added all 3 environment variables
- Run from the correct directory (project root)

### Issue: "ModuleNotFoundError: No module named 'spotipy'"
**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate
# Then reinstall
pip install -r requirements.txt
```

### Issue: "Authorization failed" or "Token expired"
**Solution**:
```bash
# Delete cache and re-authenticate
rm .spotify_cache
python3 -m app  # Run again
```

### Issue: "Port 5000 is already in use"
**Solution**:
```bash
# Change port in app/__main__.py
# Change: app.run(debug=True)
# To:     app.run(debug=True, port=5001)
```

### Issue: "CORS" errors when calling from frontend
**Solution**:
- CORS is already enabled in the app (Flask-CORS)
- Make sure you're calling the correct URL
- Check browser console for specific error

---

## Development Workflow

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Start Flask Server
```bash
python3 -m app
```

### 3. Test Endpoints
Use curl, Postman, or your browser to test endpoints

### 4. View Logs
Logs appear in the terminal where you ran the app

### 5. Stop Server
Press `Ctrl+C` in the terminal

---

## File Structure During Execution

```
spotify-visualizer/
├── .env                      # Your secret credentials (NEVER commit)
├── .spotify_cache            # OAuth token cache (auto-generated)
├── .spotify_cache-<user>     # Alt cache location
├── recent_tracks.csv         # Generated by retrieve.py
├── venv/                     # Virtual environment (do NOT commit)
├── app/
│   ├── __init__.py
│   ├── __main__.py           # Entry point
│   ├── routes.py
│   └── services/
│       ├── spotify_client.py
│       └── spotify_data.py
└── retrieve.py               # Standalone script
```

---

## Quick Start Checklist

- [ ] Python 3.9+ installed
- [ ] Created Spotify Developer app
- [ ] Got Client ID, Client Secret, Redirect URI
- [ ] Cloned repository
- [ ] Created `.env` file with credentials
- [ ] Created virtual environment (`python3 -m venv venv`)
- [ ] Activated virtual environment (`source venv/bin/activate`)
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Run Flask app (`python3 -m app`)
- [ ] Test endpoint in browser (`http://localhost:5000/user`)

---

## Next Steps

After successful execution:
1. Explore different endpoints
2. Check `ARCHITECTURE.md` for project structure
3. Consider adding a frontend (React, Vue, etc.)
4. Add data visualization (matplotlib, plotly)
5. Build more advanced analytics features
