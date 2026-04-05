import { useEffect, useState } from "react"
import { fetchTopArtists } from "../api/spotify"
import ArtistList from "../components/ArtistList"
import PeriodPills from "../components/PeriodPills"

export default function TopArtists({ token }) {
  const [artists, setArtists] = useState([])
  const [period, setPeriod] = useState("month")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    fetchTopArtists(token, period)
      .then(setArtists)
      .catch(() => setError("Failed to load top artists."))
      .finally(() => setLoading(false))
  }, [token, period])

  if (error) return <p style={{ color: "red" }}>{error}</p>

  return (
    <div>
      <PeriodPills period={period} setPeriod={setPeriod} />
      {loading ? <p style={{ color: "#888" }}>Loading...</p> : <ArtistList artists={artists} />}
    </div>
  )
}