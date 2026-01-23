import React from "react";
import "../styles/ConferenceManage.css";

const ConferenceManage = () => {
  return (
    <div className="admin-page">
      {/* ===== HEADER ===== */}
      <header className="admin-header">
        <div className="logo">UTH - COMFMS</div>
        <div className="admin-user">NGUYEN VAN A</div>
      </header>

      {/* ===== BODY ===== */}
      <div className="admin-body">
        {/* ===== SIDEBAR ===== */}
        <aside className="admin-sidebar">
          <div className="menu-item active">Quản lí đa hội nghị</div>
          <div className="menu-item">Phân quyền theo vai trò và tenant</div>
          <div className="menu-item">Bảo trì hệ thống</div>
          <div className="menu-item">Quản trị AI</div>
        </aside>

        {/* ===== CONTENT ===== */}
        <main className="admin-content">
          <div className="content-card">
            {/* Tabs */}
            <div className="conference-tabs">
              <div className="tab active">Tạo hội nghị</div>
              <div className="tab">Cập nhật hội nghị</div>
              <div className="tab">Xóa hội nghị</div>
              <div className="tab">Danh sách hội nghị</div>
            </div>

            {/* Form */}
            <div className="conference-form">
              <div className="form-row">
                <label>Tên hội nghị</label>
                <input type="text" />
              </div>

              <div className="form-row">
                <label>Khoa</label>
                <input type="text" />
              </div>

              <div className="form-row">
                <label>Định dạng file</label>
                <input type="text" />
              </div>

              <div className="form-row">
                <label>Thời gian</label>
                <input type="text" />
              </div>

              <div className="form-row">
                <label>Mô tả</label>
                <textarea />
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default ConferenceManage;
