import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/EditUser.css";

// Cấu hình quyền theo hệ thống quản lý hội nghị
const ROLE_PERMISSIONS = {
  "Author": {
    submitPaper: true,
    editSubmission: true,
    viewDecision: true,
    uploadCameraReady: true,
  },
  "Reviewer/PC Member": {
    acceptAssignment: true,
    submitReview: true,
    viewAssignedPapers: true,
    internalDiscussion: true,
  },
  "Program/Track Chair": {
    configureConference: true,
    assignPapers: true,
    makeDecision: true,
    monitorProgress: true,
  },
  "Admin": {
    manageConference: true,
    manageUser: true,
    systemMaintenance: true,
    manageAIGovernance: true,
  }
};

const EditUser = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState("Author");
  const [permissions, setPermissions] = useState(ROLE_PERMISSIONS["Author"]);

  useEffect(() => {
    setPermissions(ROLE_PERMISSIONS[role]);
  }, [role]);

  const handlePermissionChange = (key) => {
    setPermissions({
      ...permissions,
      [key]: !permissions[key],
    });
  };

  const handleSave = () => {
    // Giả lập lưu dữ liệu
    alert("Lưu thành công!");

    // Điều hướng về trang danh sách người dùng
    navigate("/conference-manage");
  };

  const handleCancel = () => {
    navigate("/conference-manage");
  };

  const renderPermissionLabel = (key) => {
    const map = {
      submitPaper: "Nộp bài báo",
      editSubmission: "Chỉnh sửa bài đã nộp",
      viewDecision: "Xem kết quả",
      uploadCameraReady: "Tải bản camera-ready",

      acceptAssignment: "Chấp nhận phân công phản biện",
      submitReview: "Nộp nhận xét phản biện",
      viewAssignedPapers: "Xem bài được giao",
      internalDiscussion: "Tham gia thảo luận nội bộ",

      configureConference: "Cấu hình hội nghị",
      assignPapers: "Phân công bài",
      makeDecision: "Ra quyết định",
      monitorProgress: "Theo dõi tiến độ",

      manageConference: "Quản lý hội nghị",
      manageUser: "Quản lý người dùng",
      systemMaintenance: "Bảo trì hệ thống",
      manageAIGovernance: "Quản trị chức năng AI",
    };
    return map[key] || key;
  };

  return (
    <div className="edit-user-container">
      <h2>Chỉnh sửa người dùng</h2>

      <div className="form-group">
        <label>Vai trò</label>
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="Author">Author – Tác giả</option>
          <option value="Reviewer/PC Member">Reviewer / PC Member</option>
          <option value="Program/Track Chair">Program/Track Chair</option>
          <option value="Admin">Admin</option>
        </select>
      </div>

      <div className="permission-box">
        <h3>Phân quyền theo vai trò</h3>

        {Object.keys(permissions).map((key) => (
          <label key={key}>
            <input
              type="checkbox"
              checked={permissions[key]}
              onChange={() => handlePermissionChange(key)}
            />
            {renderPermissionLabel(key)}
          </label>
        ))}
      </div>

      <div className="action-btn">
        <button className="btn-save" onClick={handleSave}>Lưu</button>
        <button className="btn-cancel" onClick={handleCancel}>Hủy</button>
      </div>
    </div>
  );
};

export default EditUser;