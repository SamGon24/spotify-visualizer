export default function Header({ user }) {
  if (!user) return null

  const avatar = user.images?.[0]?.url
  const initials = user.display_name
    ?.split(" ")
    .map((w) => w[0])
    .join("")
    .toUpperCase()
    .slice(0, 2)

  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      gap: "14px",
      padding: "1.5rem 2rem",
      borderBottom: "0.5px solid #e0e0e0",
    }}>
      {avatar ? (
        <img
          src={avatar}
          alt="avatar"
          style={{ width: 44, height: 44, borderRadius: "50%", objectFit: "cover" }}
        />
      ) : (
        <div style={{
          width: 44,
          height: 44,
          borderRadius: "50%",
          background: "#e8f4fd",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 14,
          fontWeight: 500,
          color: "#1a73e8",
        }}>
          {initials}
        </div>
      )}
      <div>
        <div style={{ fontSize: 16, fontWeight: 500 }}>{user.display_name}</div>
        <div style={{ fontSize: 13, color: "#888", marginTop: 2 }}>
          Spotify {user.product} · {user.country}
        </div>
      </div>
    </div>
  )
}