export default function ArtistList({ artists }) {
  if (!artists || artists.length === 0) {
    return <p style={{ color: "#888" }}>No artists found.</p>
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "2px" }}>
      {artists.map((artist, i) => (
        <a
          key={artist.id ?? i}
          href={artist.external_url}
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
            {artist.images?.[0]?.url ? (
              <img
                src={artist.images[0].url}
                alt={artist.name}
                style={{ width: 38, height: 38, borderRadius: "50%", objectFit: "cover" }}
              />
            ) : (
              <div style={{ width: 38, height: 38, borderRadius: "50%", background: "#eee" }} />
            )}
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 14, fontWeight: 500, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                {artist.name}
              </div>
              <div style={{ fontSize: 12, color: "#888", marginTop: 2 }}>
                {artist.genres?.slice(0, 2).join(", ")}
              </div>
            </div>
            {artist.plays_last_7_days && (
              <div style={{ fontSize: 12, color: "#aaa" }}>
                {artist.plays_last_7_days} plays
              </div>
            )}
          </div>
        </a>
      ))}
    </div>
  )
}