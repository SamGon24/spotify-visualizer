export default function TrackList({ tracks }) {
  if (!tracks || tracks.length === 0) {
    return <p style={{ color: "#888" }}>No tracks found.</p>
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "2px" }}>
      {tracks.map((track, i) => (
        <a
          key={track.id ?? i}
          href={track.external_url}
          target="_blank"
          rel="noreferrer"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "14px",
              padding: "10px 12px",
              borderRadius: "8px",
              cursor: "pointer",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.background = "#f5f5f5")}
            onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
          >
            <div style={{ fontSize: 13, color: "#aaa", width: 16, textAlign: "right" }}>
              {i + 1}
            </div>
            {track.image ? (
              <img
                src={track.image}
                alt={track.name}
                style={{ width: 38, height: 38, borderRadius: 4, objectFit: "cover" }}
              />
            ) : (
              <div style={{ width: 38, height: 38, borderRadius: 4, background: "#eee" }} />
            )}
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 14, fontWeight: 500, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                {track.name}
              </div>
              <div style={{ fontSize: 12, color: "#888", marginTop: 2 }}>
                {Array.isArray(track.artists) ? track.artists.join(", ") : track.artists}
              </div>
            </div>
            {track.plays_last_7_days && (
              <div style={{ fontSize: 12, color: "#aaa" }}>
                {track.plays_last_7_days} plays
              </div>
            )}
          </div>
        </a>
      ))}
    </div>
  )
}