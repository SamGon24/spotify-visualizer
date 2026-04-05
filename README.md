# Spotify Visualizer

A full-stack web application that visualizes your Spotify listening habits. Built with a Python/Flask backend and a React frontend, it uses the Spotify Web API to display your recently played tracks, top tracks, and top artists across different time periods.

---

## Tech Stack

**Backend**
- Python 3.14
- Flask 3.1
- Spotipy 2.24
- Flask-CORS

**Frontend**
- React 18 (Vite)
- Axios

---

## Project Overview

Spotify Visualizer authenticates users via Spotify OAuth 2.0 and displays personalized listening data including:

- Recently played tracks
- Top tracks by time period (week, month, 6 months, year)
- Top artists by time period (week, month, 6 months, year)

The backend handles Spotify authentication and proxies API requests. The frontend consumes the Flask API using a Bearer token passed through request headers.

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Spotify Developer account

### 1. Clone the repository
```bash
git clone https://github.com/SamGon24/spotify-visualizer.git
cd spotify-visualizer
```

### 2. Create a Spotify App
- Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
- Create a new app
- Add `http://127.0.0.1:5000/callback` as a Redirect URI
- Copy your Client ID and Client Secret

### 3. Set up the backend
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:5000/callback

### 4. Set up the frontend
```bash
cd frontend
npm install
```

### 5. Run the app

Terminal 1 — Flask backend:
```bash
python3 app.py
```

Terminal 2 — React frontend:
```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173` and log in with Spotify.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/login` | Initiates Spotify OAuth flow |
| GET | `/callback` | Handles Spotify OAuth callback |
| GET | `/user` | Returns current user info |
| GET | `/recent` | Returns last 10 recently played tracks |
| GET | `/top/tracks/<period>` | Returns top tracks for a given period |
| GET | `/top/artists/<period>` | Returns top artists for a given period |

Valid periods: `week`, `month`, `6months`, `year`

All endpoints except `/login` and `/callback` require an `Authorization: Bearer <token>` header.

---

## Roadmap

- [ ] Deploy backend to Railway or Render
- [ ] Deploy frontend to Vercel or Netlify
- [ ] Add listening history charts and data visualizations
- [ ] Add genre breakdown
- [ ] Token refresh handling for longer sessions
- [ ] Support for multiple users

---

## Author

Samuel Gonzalez — [github.com/SamGon24](https://github.com/SamGon24)
