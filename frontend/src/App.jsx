import { useState, useEffect } from 'react'
import './App.css'
import Header from './components/Header'
import Tabs from './components/Tabs'
import RecentlyPlayed from './pages/RecentlyPlayed'
import TopTracks from './pages/TopTracks'
import TopArtists from './pages/TopArtists'
import { fetchUser } from './api/spotify'
import Charts from './pages/Charts'


function App() {
  const [token, setToken] = useState(null)
  const [user, setUser] = useState(null)
  const [activeTab, setActiveTab] = useState('recent')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const urlToken = params.get('token')
    const urlRefresh = params.get('refresh')
    const urlExpiresIn = params.get('expires_in')

    if (urlToken) {
      const expiry = Date.now() + Number(urlExpiresIn || 3600) * 1000
      localStorage.setItem('spotify_token', urlToken)
      localStorage.setItem('spotify_refresh', urlRefresh || '')
      localStorage.setItem('spotify_expiry', String(expiry))
      setToken(urlToken)
      window.history.replaceState({}, document.title, window.location.pathname)
      return
    }

    // Restore session from localStorage if token hasn't expired
    const storedToken = localStorage.getItem('spotify_token')
    const storedExpiry = Number(localStorage.getItem('spotify_expiry') || 0)
    if (storedToken && Date.now() < storedExpiry) {
      setToken(storedToken)
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('spotify_token')
    localStorage.removeItem('spotify_refresh')
    localStorage.removeItem('spotify_expiry')
    setToken(null)
    setUser(null)
  }

  useEffect(() => {
    if (token) {
      setLoading(true)
      setError(null)
      fetchUser(token)
        .then((userData) => {
          setUser(userData)
        })
        .catch((err) => {
          setError('Failed to fetch user data. Please try logging in again.')
          console.error(err)
        })
        .finally(() => setLoading(false))
    }
  }, [token])

  if (!token) {
    return (
      <div className="app">
        <div className="container">
          <div className="app-header">
            <h1>🎵 Spotify Visualizer</h1>
            <p>Visualize your Spotify listening habits</p>
            <a href={`${import.meta.env.VITE_API_URL}/login`} style={{ marginTop: '20px', display: 'inline-block' }}>
              <button style={{
                padding: '12px 30px',
                fontSize: '1em',
                backgroundColor: '#1db954',
                color: 'white',
                border: 'none',
                borderRadius: '30px',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}>
                Login with Spotify
              </button>
            </a>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <Header user={user} onLogout={handleLogout} />
      <div className="container">
        {error && <div className="error">{error}</div>}
        {loading && <div className="loading">Loading...</div>}
        {!loading && (
          <>
            <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
            {activeTab === 'recent' && <RecentlyPlayed token={token} />}
            {activeTab === 'tracks' && <TopTracks token={token} />}
            {activeTab === 'artists' && <TopArtists token={token} />}
            {activeTab === 'charts' && <Charts token={token} />} 
          </>
        )}
      </div>
    </div>
  )
}

export default App