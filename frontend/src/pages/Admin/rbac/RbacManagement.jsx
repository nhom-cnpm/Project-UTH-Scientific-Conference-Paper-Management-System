// src/pages/Admin/rbac/RbacManagement.jsx

import React, { useEffect, useState } from "react";
import { adminApi } from "../../../services/Rbac"; // Đảm bảo import đúng đường dẫn
import "../../../styles/AdminQuanli.css";

const RbacManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false); // Đổi mặc định để tránh lỗi giao diện nếu fetch quá nhanh

  useEffect(() => {
    setLoading(true);
    adminApi.getUsers().then((data) => {
      setUsers(data);
      setLoading(false);
    });
  }, []);

  const handleRoleChange = (userId, newRole) => {
    adminApi.updateUserRole(userId, newRole).then(() => {
      // Cập nhật State cục bộ sau khi "API" giả lập trả về thành công
      setUsers((prev) =>
        prev.map((u) =>
          u.id === userId ? { ...u, role: newRole } : u
        )
      );
      alert(`Đã cập nhật quyền thành: ${newRole}`);
    });
  };

  if (loading) return <p className="loading">Đang tải danh sách người dùng...</p>;

  return (
    <div className="rbac-container">
      <h2>Phân quyền & Quản lý Tenant</h2>

      <table className="rbac-table">
        <thead>
          <tr>
            <th>Người dùng</th>
            <th>Email</th>
            <th>Tenant (Đơn vị)</th>
            <th>Vai trò</th>
            <th>Trạng thái</th>
          </tr>
        </thead>

        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.name}</td>
              <td>{u.email}</td>
              <td>{u.tenant}</td>
              <td>
                <select
                  className="role-select"
                  value={u.role}
                  onChange={(e) => handleRoleChange(u.id, e.target.value)}
                >
                  <option value="Admin">Admin</option>
                  <option value="Chair">Chair</option>
                  <option value="Reviewer">Reviewer</option>
                  <option value="Student">Student</option>
                </select>
              </td>
              <td>
                <span className={`status-badge ${u.status}`}>
                  {u.status === "active" ? "Hoạt động" : "Khóa"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RbacManagement;