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

  /* ===== RBAC STATE ===== */
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(mockUsers.length / USERS_PER_PAGE);
  const startIndex = (currentPage - 1) * USERS_PER_PAGE;
  const currentUsers = mockUsers.slice(
    startIndex,
    startIndex + USERS_PER_PAGE
  );

  return (
    <div className="admin-layout">
      {/* ===== SIDEBAR ===== */}
      <aside className="admin-sidebar">
        <h2 className="logo">UTH - COMFMS</h2>

        <ul className="sidebar-menu">
          <li
            className={activeMenu === "conference" ? "active" : ""}
            onClick={() => setActiveMenu("conference")}
          >
            Quản lí hội nghị
          </li>
          <li
            className={activeMenu === "rbac" ? "active" : ""}
            onClick={() => setActiveMenu("rbac")}
          >
            Phân quyền theo vai trò & tenant
          </li>
          <li>Bảo trì hệ thống</li>
          <li>Quản trị AI</li>
        </ul>
      </aside>

      {/* ===== MAIN ===== */}
      <main className="admin-main">
        {/* ===================== QUẢN LÍ HỘI NGHỊ ===================== */}
        {activeMenu === "conference" && (
          <>
            {/* TABS */}
            <div className="conf-tabs">
              {["create", "update", "delete", "list"].map((tab) => (
                <button
                  key={tab}
                  className={activeTab === tab ? "tab active" : "tab"}
                  onClick={() => setActiveTab(tab)}
                >
                  {{
                    create: "Tạo hội nghị",
                    update: "Cập nhật hội nghị",
                    delete: "Xóa hội nghị",
                    list: "Danh sách hội nghị",
                  }[tab]}
                </button>
              ))}
            </div>

            {/* CONTENT */}
            <div className="conf-content">
              {activeTab === "create" && (
                <div className="form-box">
                  <div className="form-group">
                    <label>Tên hội nghị</label>
                    <input type="text" />
                  </div>

                  <div className="form-group">
                    <label>Khoa</label>
                    <input type="text" />
                  </div>

                  <div className="form-group">
                    <label>Định dạng file</label>
                    <input type="text" />
                  </div>

                  <div className="form-group">
                    <label>Thời gian</label>
                    <input type="date" />
                  </div>

                  <div className="form-group">
                    <label>Mô tả</label>
                    <textarea rows="4" />
                  </div>

                  <button className="btn-primary">Tạo hội nghị</button>
                </div>
              )}

              {activeTab !== "create" && (
                <p className="hint-text">
                  (Danh sách hội nghị sẽ hiển thị tại đây)
                </p>
              )}
            </div>
          </>
        )}

        {/* ===================== PHÂN QUYỀN ===================== */}
        {activeMenu === "rbac" && (
          <>
            <div className="rbac-header">
              <h3>Quản lí người dùng</h3>
              <button className="btn-primary">+ Thêm người dùng</button>
            </div>

            <table className="rbac-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Email</th>
                  <th>Tenant</th>
                  <th>Trạng thái</th>
                  <th>Hành động</th>
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
                    <td className="action">Edit</td>
                    <td className="action">
                      <Link to={`/conference-manage/Edit/${u.id}`} className="edit-link">
                      Edit
                      </Link>
                      </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* PAGINATION */}
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
      </main>
    </div>
  );
};

export default ConferenceManage;
