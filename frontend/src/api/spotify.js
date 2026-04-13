import axios from "axios"

const BASE = import.meta.env.VITE_API_URL

const client = axios.create({ baseURL: BASE })

export const getToken = () => localStorage.getItem("spotify_token")

const authHeader = (token) => ({
  headers: { Authorization: `Bearer ${token}` },
})

// Auto-refresh on 401: swap in new token and retry the original request once
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      const refreshToken = localStorage.getItem("spotify_refresh")
      if (!refreshToken) return Promise.reject(error)

      try {
        const { data } = await axios.get(`${BASE}/refresh`, {
          params: { refresh_token: refreshToken },
        })
        const newToken = data.access_token
        const newExpiry = Date.now() + (data.expires_in || 3600) * 1000
        localStorage.setItem("spotify_token", newToken)
        localStorage.setItem("spotify_expiry", String(newExpiry))
        original.headers["Authorization"] = `Bearer ${newToken}`
        return client(original)
      } catch {
        // Refresh failed — clear session so user sees login screen
        localStorage.removeItem("spotify_token")
        localStorage.removeItem("spotify_refresh")
        localStorage.removeItem("spotify_expiry")
        window.location.href = "/"
        return Promise.reject(error)
      }
    }
    return Promise.reject(error)
  }
)

export const fetchUser = (token) =>
  client.get("/user", authHeader(token)).then((r) => r.data.data)

export const fetchRecentlyPlayed = (token) =>
  client.get("/recent", authHeader(token)).then((r) => r.data.data)

export const fetchTopTracks = (token, period) =>
  client.get(`/top/tracks/${period}`, authHeader(token)).then((r) => r.data.data)

export const fetchTopArtists = (token, period) =>
  client.get(`/top/artists/${period}`, authHeader(token)).then((r) => r.data.data)
