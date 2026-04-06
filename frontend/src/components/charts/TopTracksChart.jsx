import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts"

export default function TopTracksChart({ tracks }) {
  if (!tracks || tracks.length === 0) {
    return <p style={{ color: "#888" }}>No data available.</p>
  }

  const data = tracks
    .filter((t) => t.plays_last_7_days)
    .map((t) => ({
      name: t.name.length > 20 ? t.name.slice(0, 20) + "…" : t.name,
      plays: t.plays_last_7_days,
    }))

  if (data.length === 0) {
    return <p style={{ color: "#888" }}>No play count data — try the week period.</p>
  }

  return (
    <div style={{ width: "100%", height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 60 }}>
          <XAxis dataKey="name" angle={-35} textAnchor="end" tick={{ fontSize: 12 }} />
          <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
          <Tooltip />
          <Bar dataKey="plays" fill="#1db954" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}