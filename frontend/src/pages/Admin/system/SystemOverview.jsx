import React from "react";
import { useNavigate } from "react-router-dom";

const SystemOverview = () => {
  const navigate = useNavigate();

  return (
    <div className="system-grid">
      <div className="system-card" onClick={() => navigate("smtp")}>
        <h4>SMTP Configuration</h4>
        <p>Thiết lập server gửi mail</p>
      </div>

      {/* Sửa từ "quota" thành "email-quota" cho khớp App.js */}
      <div className="system-card" onClick={() => navigate("email-quota")}>
        <h4>Email Quota</h4>
        <p>Quản lý định mức gửi mail</p>
      </div>

      {/* Sửa từ "logs" thành "audit-logs" cho khớp App.js */}
      <div className="system-card" onClick={() => navigate("audit-logs")}>
        <h4>Audit Logs</h4>
        <p>Xem nhật ký hoạt động</p>
      </div>

      <div className="system-card" onClick={() => navigate("backup")}>
        <h4>Backup</h4>
        <p>Sao lưu dữ liệu hệ thống</p>
      </div>

      <div className="system-card warning" onClick={() => navigate("restore")}>
        <h4>Restore</h4>
        <p>Khôi phục dữ liệu</p>
      </div>
    </div>
  );
};

export default SystemOverview;