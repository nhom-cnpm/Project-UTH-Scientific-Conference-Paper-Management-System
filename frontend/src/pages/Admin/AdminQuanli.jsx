import React, { useEffect, useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import { adminApi } from "../../services/adminApi";
import "../../styles/AdminQuanli.css";


const AdminQuanli = () => {
  const [overview, setOverview] = useState(null);

  useEffect(() => {
  const load = async () => {
    try {
      const data = await adminApi.getDashboardOverview();
      setOverview(data);
    } catch (err) {
      console.error("Không lấy được dashboard overview:", err);
      setOverview(null); // không hiển thị gì
    }
  };

  load();
}, []);


  return (
    <div className="admin-container">
      <aside className="admin-sidebar">
        <h2 className="admin-logo">ADMIN PANEL</h2>

        {overview && (
          <div className="admin-summary">
            <p>Users: {overview.totalUsers}</p>
            <p>Conferences: {overview.totalConferences}</p>
            <p>System: {overview.systemStatus}</p>
            <p>AI: {overview.aiEnabled ? "ON" : "OFF"}</p>
          </div>
        )}

        <nav className="admin-menu">
          <NavLink to="">Hội nghị</NavLink>
          <NavLink to="rbac">RBAC</NavLink>
          <NavLink to="system">System</NavLink>
          <NavLink to="ai">AI</NavLink>
          </nav>

      </aside>

      <main className="admin-content">
        <Outlet />
      </main>
    </div>
  );
};

export default AdminQuanli;
