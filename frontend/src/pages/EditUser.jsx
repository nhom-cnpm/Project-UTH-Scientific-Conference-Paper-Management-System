import React, { useState } from "react";
import "../styles/EditUser.css";

const EditUser = () => {
  const [role, setRole] = useState("Giảng viên");

  const [permissions, setPermissions] = useState({
    viewReport: true,
    approveReport: false,
    createEvent: false,
    manageUser: false,
  });

  const handlePermissionChange = (key) => {
    setPermissions({
      ...permissions,
      [key]: !permissions[key],
    });
  };

  return (
    <div className="edit-user-container">
      <h2>Chỉnh sửa người dùng</h2>

      {/* ROLE */}
      <div className="form-group">
        <label>Vai trò</label>
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option>Sinh viên</option>
          <option>Giảng viên</option>
          <option>Quản trị viên</option>
        </select>
      </div>

      {/* PERMISSION */}
      <div className="permission-box">
        <h3>Phân quyền</h3>

        <label>
          <input
            type="checkbox"
            checked={permissions.viewReport}
            onChange={() => handlePermissionChange("viewReport")}
          />
          Xem báo cáo khoa học
        </label>

        <label>
          <input
            type="checkbox"
            checked={permissions.approveReport}
            onChange={() => handlePermissionChange("approveReport")}
          />
          Duyệt báo cáo
        </label>

        <label>
          <input
            type="checkbox"
            checked={permissions.createEvent}
            onChange={() => handlePermissionChange("createEvent")}
          />
          Tạo sự kiện khoa học
        </label>

        <label>
          <input
            type="checkbox"
            checked={permissions.manageUser}
            onChange={() => handlePermissionChange("manageUser")}
          />
          Quản lý người dùng
        </label>
      </div>

      {/* ACTION */}
      <div className="action-btn">
        <button className="btn-save">Lưu</button>
        <button className="btn-cancel">Hủy</button>
      </div>
    </div>
  );
};

export default EditUser;
