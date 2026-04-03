import { useEffect, useState } from "react"
import { fetchRecentlyPlayed } from "../api/spotify"
import TrackList from "../components/TrackList"

export default function RecentlyPlayed({ token }) {
  const [tracks, setTracks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchRecentlyPlayed(token)
      .then(setTracks)
      .catch(() => setError("Failed to load recently played."))
      .finally(() => setLoading(false))
  }, [token])

  if (loading) return <p style={{ color: "#888" }}>Loading...</p>
  if (error) return <p style={{ color: "red" }}>{error}</p>

  return <TrackList tracks={tracks} />
}