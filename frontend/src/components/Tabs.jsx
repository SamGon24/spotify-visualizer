const TABS = [
  { label: "Recently played", value: "recent" },
  { label: "Top tracks", value: "tracks" },
  { label: "Top artists", value: "artists" },
]

export default function Tabs({ activeTab, setActiveTab }) {
  return (
    <div style={{
      display: "flex",
      gap: "4px",
      borderBottom: "0.5px solid #e0e0e0",
      marginBottom: "1.5rem",
    }}>
      {TABS.map((tab) => (
        <button
          key={tab.value}
          onClick={() => setActiveTab(tab.value)}
          style={{
            padding: "8px 16px",
            fontSize: 14,
            background: "transparent",
            border: "none",
            borderBottom: activeTab === tab.value ? "2px solid #111" : "2px solid transparent",
            color: activeTab === tab.value ? "#111" : "#888",
            fontWeight: activeTab === tab.value ? 500 : 400,
            cursor: "pointer",
            marginBottom: "-0.5px",
          }}
        >
          {tab.label}
        </button>
      ))}
    </div>
  )
}