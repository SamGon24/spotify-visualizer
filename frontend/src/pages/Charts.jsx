import { useEffect, useState } from "react"
import { fetchTopTracks } from "../api/spotify"
import TopTracksChart from "../components/charts/TopTracksChart"

export default function Charts({ token }) {
  const [tracks, setTracks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchTopTracks(token, "week")
      .then((data) => {
        console.log("tracks data:", data)
        setTracks(data)
      })
      .catch((err) => {
        console.error(err)
        setError("Failed to load chart data.")
      })
      .finally(() => setLoading(false))
  }, [token])

  if (loading) return <p style={{ color: "#888" }}>Loading charts...</p>
  if (error) return <p style={{ color: "red" }}>{error}</p>

  return (
    <div style={{ padding: "1rem 0" }}>
      <h2 style={{ fontSize: 16, fontWeight: 500, marginBottom: "1rem" }}>
        Top tracks this week
      </h2>
      <TopTracksChart tracks={tracks} />
    </div>
  )
}