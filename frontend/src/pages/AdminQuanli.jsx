import React, { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/AdminQuanli.css";

const USERS_PER_PAGE = 10;

/* ===== MOCK USERS ===== */
const mockUsers = Array.from({ length: 20 }, (_, i) => ({
  id: i + 1,
  name: `Nguyen Van ${String.fromCharCode(65 + i)}`,
  email: `user${i + 1}@ut.edu.vn`,
  tenant: i < 10 ? "Tenant A" : "Tenant B",
  role: i % 3 === 0 ? "Admin" : i % 3 === 1 ? "Reviewer" : "Student",
  status: i % 2 === 0 ? "online" : "offline",
}));

const ConferenceManage = () => {
  /* ===== SIDEBAR STATE ===== */
  const [activeMenu, setActiveMenu] = useState("conference");

  /* ===== CONFERENCE STATE ===== */
  const [activeTab, setActiveTab] = useState("create");

  /* ===== SYSTEM MAINTENANCE STATE ===== */
  const [systemTab, setSystemTab] = useState("overview");

  /* ===== RBAC STATE ===== */
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(mockUsers.length / USERS_PER_PAGE);
  const startIndex = (currentPage - 1) * USERS_PER_PAGE;
  const currentUsers = mockUsers.slice(
    startIndex,
    startIndex + USERS_PER_PAGE
  );
  /* ===== AI ADMINISTRATION STATE ===== */
const [aiTab, setAiTab] = useState("overview");
const [aiEnabled, setAiEnabled] = useState(true);

  return (
    <div className="admin-layout">
      {/* ===== SIDEBAR ===== */}
      <aside className="admin-sidebar">
        <Link to="/" className="logo-link">
        <div className="logo">UTH - COMFMS</div>
        </Link>

        <ul className="sidebar-menu">
          <li
            className={activeMenu === "conference" ? "active" : ""}
            onClick={() => setActiveMenu("conference")}
          >
            Conference Management
          </li>

          <li
            className={activeMenu === "rbac" ? "active" : ""}
            onClick={() => setActiveMenu("rbac")}
          >
            RBAC & Tenant Roles
          </li>

          <li
            className={activeMenu === "system" ? "active" : ""}
            onClick={() => {
              setActiveMenu("system");
              setSystemTab("overview");
            }}
          >
            System Maintenance
          </li>

          <li
  className={activeMenu === "ai" ? "active" : ""}
  onClick={() => {
    setActiveMenu("ai");
    setAiTab("overview");
  }}
>
  AI Administration
</li>
        </ul>
      </aside>

      {/* ===== MAIN ===== */}
      <main className="admin-main">
        {/* ===================== CONFERENCE MANAGEMENT ===================== */}
        {activeMenu === "conference" && (
          <>
            <div className="conf-tabs">
              {["create", "update", "delete", "list"].map((tab) => (
                <button
                  key={tab}
                  className={activeTab === tab ? "tab active" : "tab"}
                  onClick={() => setActiveTab(tab)}
                >
                  {{
                    create: "Create Conference",
                    update: "Update Conference",
                    delete: "Delete Conference",
                    list: "Conference List",
                  }[tab]}
                </button>
              ))}
            </div>

            <div className="conf-content">
              {activeTab === "create" && (
                <div className="form-box">
                  <div className="form-group">
                    <label>Conference Name</label>
                    <input type="text" />
                  </div>

                  <div className="form-group">
                    <label>Department / Faculty</label>
                    <input type="text" />
                  </div>

                  <div className="form-group">
                    <label>File Formats Allowed</label>
                    <input type="text" placeholder="e.g. .pdf, .docx" />
                  </div>

                  <div className="form-group">
                    <label>Event Date</label>
                    <input type="date" />
                  </div>

                  <div className="form-group">
                    <label>Description</label>
                    <textarea rows="4" />
                  </div>

                  <button className="btn-primary">Create Conference</button>
                </div>
              )}

              {activeTab !== "create" && (
                <p className="hint-text">(Conference list will be displayed here)</p>
              )}
            </div>
          </>
        )}

        {/* ===================== RBAC ===================== */}
        {activeMenu === "rbac" && (
          <>
            <div className="rbac-header">
              <h3>User Management</h3>
              <button className="btn-primary">+ Add User</button>
            </div>

            <table className="rbac-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Email</th>
                  <th>Tenant</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {currentUsers.map((u) => (
                  <tr key={u.id}>
                    <td>{u.name}</td>
                    <td>{u.email}</td>
                    <td>{u.tenant}</td>
                    <td>
                      <span className={`status ${u.status}`}>
                        {u.status}
                      </span>
                    </td>
                    <td>
                     <Link to={`/edituser/${u.id}`} className="edit-link">
                     Edit
                     </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="pagination">
              <button
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(currentPage - 1)}
              >
                &lt;
              </button>
              <span>
                {currentPage} / {totalPages}
              </span>
              <button
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage(currentPage + 1)}
              >
                &gt;
              </button>
            </div>
          </>
        )}

        {/* ===================== SYSTEM MAINTENANCE ===================== */}
        {activeMenu === "system" && (
          <div className="system-wrapper">
            <h3 className="system-title">System Configuration & Maintenance</h3>

            {/* ===== OVERVIEW ===== */}
            {systemTab === "overview" && (
              <div className="system-grid">
                <div
                  className="system-card clickable"
                  onClick={() => setSystemTab("smtp")}
                >
                  <h4>Configure SMTP</h4>
                  <p>Setup outgoing email server</p>
                </div>

                <div
                  className="system-card clickable"
                  onClick={() => setSystemTab("quota")}
                >
                  <h4>Manage Email Quota</h4>
                  <p>Manage email sending limits</p>
                </div>

                <div
                  className="system-card clickable"
                  onClick={() => setSystemTab("logs")}
                >
                  <h4>View Audit Logs</h4>
                  <p>View system activity logs</p>
                </div>

                <div
                  className="system-card clickable"
                  onClick={() => setSystemTab("backup")}
                >
                  <h4>Backup System</h4>
                  <p>Create a system data backup</p>
                </div>

                <div
                  className="system-card warning clickable"
                  onClick={() => setSystemTab("restore")}
                >
                  <h4>Restore System</h4>
                  <p>Restore data from a backup file</p>
                </div>
              </div>
            )}

            {/* ===== SMTP CONFIG ===== */}
            {systemTab === "smtp" && (
              <div className="smtp-box">
                <button className="back-btn" onClick={() => setSystemTab("overview")}>
                  ← Back
                </button>

                <h4>SMTP Server Configuration</h4>

                <div className="smtp-form">
                  <div className="smtp-row">
                    <label>SMTP Host</label>
                    <input type="text" placeholder="smtp.gmail.com" />
                  </div>

                  <div className="smtp-row">
                    <label>SMTP Port</label>
                    <input type="number" placeholder="587" />
                  </div>

                  <div className="smtp-row">
                    <label>Sender Email</label>
                    <input type="email" placeholder="no-reply@ut.edu.vn" />
                  </div>

                  <div className="smtp-row">
                    <label>App Password</label>
                    <input type="password" placeholder="********" />
                  </div>

                  <div className="smtp-row inline">
                    <label>
                      <input type="checkbox" /> Use SSL / TLS
                    </label>
                  </div>

                  <div className="smtp-actions">
                    <button className="btn-secondary">Test Email</button>
                    <button className="btn-primary">Save Configuration</button>
                  </div>
                </div>
              </div>
            )}

            {/* ===== EMAIL QUOTA ===== */}
            {systemTab === "quota" && (
              <div className="quota-box">
                <button className="back-btn" onClick={() => setSystemTab("overview")}>
                  ← Back
                </button>

                <h4>Email Quota Management</h4>

                <div className="quota-form">
                  <div className="quota-row">
                    <label>Daily Email Limit</label>
                    <input type="number" placeholder="1000" />
                  </div>

                  <div className="quota-row">
                    <label>Monthly Email Limit</label>
                    <input type="number" placeholder="30000" />
                  </div>

                  <div className="quota-row">
                    <label>Apply to Tenant</label>
                    <select>
                      <option>Tenant A</option>
                      <option>Tenant B</option>
                    </select>
                  </div>

                  <div className="quota-row inline">
                    <label>
                      <input type="checkbox" /> Allow over-limit sending
                    </label>
                  </div>

                  <div className="quota-actions">
                    <button className="btn-secondary">Reset to Default</button>
                    <button className="btn-primary">Save Quota</button>
                  </div>
                </div>
              </div>
            )}

            {/* ===== AUDIT LOGS ===== */}
            {systemTab === "logs" && (
              <div className="logs-box">
                <button className="back-btn" onClick={() => setSystemTab("overview")}>
                  ← Back
                </button>

                <h4>System Audit Logs</h4>

                <table className="logs-table">
                  <thead>
                    <tr>
                      <th>Timestamp</th>
                      <th>User</th>
                      <th>Action</th>
                      <th>IP Address</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>2026-02-04 09:12</td>
                      <td>admin@ut.edu.vn</td>
                      <td>Updated SMTP configuration</td>
                      <td>192.168.1.10</td>
                    </tr>
                    <tr>
                      <td>2026-02-03 21:40</td>
                      <td>reviewer@ut.edu.vn</td>
                      <td>User Login</td>
                      <td>192.168.1.15</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            )}

            {/* ===== BACKUP SYSTEM ===== */}
            {systemTab === "backup" && (
              <div className="backup-box">
                <button className="back-btn" onClick={() => setSystemTab("overview")}>
                  ← Back
                </button>

                <h4>System Data Backup</h4>

                <ul className="backup-list">
                  <li>Conference Data</li>
                  <li>Users & Permissions</li>
                  <li>SMTP & Email Quota Settings</li>
                </ul>

                <div className="backup-actions">
                  <button className="btn-secondary">Backup Now</button>
                  <button className="btn-primary">Download Backup File</button>
                </div>
              </div>
            )}

            {/* ===== RESTORE SYSTEM ===== */}
            {systemTab === "restore" && (
              <div className="restore-box">
                <button className="back-btn" onClick={() => setSystemTab("overview")}>
                  ← Back
                </button>

                <h4>Restore System Data</h4>

                <p className="restore-warning">
                  ⚠️ Restoration will overwrite all current data.
                </p>

                <input type="file" />

                <label className="restore-confirm">
                  <input type="checkbox" /> I confirm that I want to restore the system
                </label>

                <div className="restore-actions">
                  <button className="btn-secondary">Cancel</button>
                  <button className="btn-danger">Restore Now</button>
                </div>
              </div>
            )}
          </div>
        )}
        {/* ===================== AI ADMINISTRATION ===================== */}
{activeMenu === "ai" && (
  <div className="ai-wrapper">
    <h3 className="system-title">AI Administration</h3>

    {/* Nút quay lại (chỉ hiện khi không ở trang overview) */}
    {aiTab !== "overview" && (
      <button className="back-btn" onClick={() => setAiTab("overview")}>
        ← Back to Overview
      </button>
    )}

    {/* Màn hình lựa chọn (Cards) */}
    {aiTab === "overview" && (
      <div className="system-grid">
        <div className="system-card clickable" onClick={() => setAiTab("config")}>
          <h4>Configure AI</h4>
          <p>Setup AI features</p>
        </div>
        <div className="system-card clickable" onClick={() => setAiTab("toggle")}>
          <h4>System Status</h4>
          <p>Enable or Disable AI</p>
        </div>
        <div className="system-card clickable" onClick={() => setAiTab("logs")}>
          <h4>AI Logs</h4>
          <p>View activity history</p>
        </div>
      </div>
    )}

    {/* Màn hình Bật/Tắt AI */}
    {aiTab === "toggle" && (
      <div className="ai-box">
        <p>Current Status: <b>{aiEnabled ? "ACTIVE" : "INACTIVE"}</b></p>
        <button 
          className={aiEnabled ? "btn-danger" : "btn-primary"}
          onClick={() => setAiEnabled(!aiEnabled)}
        >
          {aiEnabled ? "Turn Off AI" : "Turn On AI"}
        </button>
      </div>
    )}

    {/* Màn hình Logs (Bảng dữ liệu) */}
    {aiTab === "logs" && (
      <table className="logs-table">
        <thead>
          <tr><th>Time</th><th>Action</th><th>Result</th></tr>
        </thead>
        <tbody>
          <tr><td>10:30 AM</td><td>Analyze Report</td><td>Success</td></tr>
        </tbody>
      </table>
    )}
  </div>
)}
      </main>
    </div>
  );
};

export default ConferenceManage;
