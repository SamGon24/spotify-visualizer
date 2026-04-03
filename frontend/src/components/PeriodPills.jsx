const PERIODS = [
  { label: "Week", value: "week" },
  { label: "Month", value: "month" },
  { label: "6 months", value: "6months" },
  { label: "Year", value: "year" },
]

export default function PeriodPills({ period, setPeriod }) {
  return (
    <div style={{ display: "flex", gap: "8px", marginBottom: "1.25rem" }}>
      {PERIODS.map((p) => (
        <button
          key={p.value}
          onClick={() => setPeriod(p.value)}
          style={{
            padding: "4px 14px",
            fontSize: 13,
            borderRadius: "999px",
            border: "0.5px solid",
            borderColor: period === p.value ? "transparent" : "#ccc",
            background: period === p.value ? "#111" : "transparent",
            color: period === p.value ? "#fff" : "#666",
            cursor: "pointer",
          }}
        >
          {p.label}
        </button>
      ))}
    </div>
  )
}