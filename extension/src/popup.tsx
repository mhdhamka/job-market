import { useState } from "react"

export default function IndexPopup() {
  return (
    <div style={{ width: 240, padding: 14, fontFamily: "sans-serif" }}>
      <h3 style={{ margin: "0 0 8px 0", color: "#2563eb", fontSize: "16px" }}>Job Tracker</h3>
      <p style={{ fontSize: "13px", color: "#4b5563", lineHeight: "1.4" }}>
        Browse JobStreet or MYFutureJobs. Use the floating button on job listings to log applications directly into your local DuckDB database.
      </p>
    </div>
  )
}