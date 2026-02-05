import React from "react";

export default function Dashboard() {
  return (
    <div className="chair-card">
      <h2>Chair Dashboard</h2>

      <div className="stat-grid">
        <div className="stat-box">
          <h4>Conferences</h4>
          <p>2</p>
        </div>

        <div className="stat-box">
          <h4>PC Members</h4>
          <p>3</p>
        </div>

        <div className="stat-box">
          <h4>Papers</h4>
          <p>2</p>
        </div>
      </div>
    </div>
  );
}
