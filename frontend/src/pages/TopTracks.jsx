import { useEffect, useState } from "react"
import { fetchTopTracks } from "../api/spotify"
import TrackList from "../components/TrackList"
import PeriodPills from "../components/PeriodPills"

export default function TopTracks({ token }) {
  const [tracks, setTracks] = useState([])
  const [period, setPeriod] = useState("month")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    fetchTopTracks(token, period)
      .then(setTracks)
      .catch(() => setError("Failed to load top tracks."))
      .finally(() => setLoading(false))
  }, [token, period])

  if (error) return <p style={{ color: "red" }}>{error}</p>

  return (
    <div>
      <PeriodPills period={period} setPeriod={setPeriod} />
      {loading ? <p style={{ color: "#888" }}>Loading...</p> : <TrackList tracks={tracks} />}
    </div>
  )
}