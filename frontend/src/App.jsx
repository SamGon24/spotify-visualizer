import axios from "axios"

const BASE = "http://localhost:5000"

const client = axios.create({ baseURL: BASE })

const authHeader = (token) => ({
  headers: { Authorization: `Bearer ${token}` },
})

export const fetchUser = (token) =>
  client.get("/user", authHeader(token)).then((r) => r.data.data)

export const fetchRecentlyPlayed = (token) =>
  client.get("/recent", authHeader(token)).then((r) => r.data.data)

export const fetchTopTracks = (token, period) =>
  client.get(`/top/tracks/${period}`, authHeader(token)).then((r) => r.data.data)

export const fetchTopArtists = (token, period) =>
  client.get(`/top/artists/${period}`, authHeader(token)).then((r) => r.data.data)