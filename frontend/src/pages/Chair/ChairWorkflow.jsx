import React, { useState } from "react";
import "../../styles/chair.css";


import Dashboard from "./Dashboard";
import PCManagement from "./PCManagement";
import AssignPapers from "./AssignPapers";
import ReviewMonitoring from "./ReviewMonitoring";
import Decision from "./Decision";

export default function ChairWorkflow() {
  const [menu, setMenu] = useState("dashboard");

  return (
    <div className="chair-layout">
      <aside className="chair-sidebar">
        <h3>Program / Track Chair</h3>

        <ul>
          <li onClick={() => setMenu("dashboard")}>Chair Dashboard</li>
          <li onClick={() => setMenu("pc")}>PC Management</li>
          <li onClick={() => setMenu("assign")}>Assign Papers</li>
          <li onClick={() => setMenu("review")}>Review Monitoring</li>
          <li onClick={() => setMenu("decision")}>Decision Making</li>
        </ul>
      </aside>

      <main className="chair-main">
        {menu === "dashboard" && <Dashboard />}
        {menu === "pc" && <PCManagement />}
        {menu === "assign" && <AssignPapers />}
        {menu === "review" && <ReviewMonitoring />}
        {menu === "decision" && <Decision />}
      </main>
    </div>
  );
}
