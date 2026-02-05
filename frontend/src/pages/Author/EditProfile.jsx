import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const EditProfile = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({});

  useEffect(() => {
    const savedProfile = JSON.parse(localStorage.getItem("authorProfile"));
    if (savedProfile) setFormData(savedProfile);
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSave = () => {
    localStorage.setItem("authorProfile", JSON.stringify(formData));
    alert("Cập nhật thông tin thành công!");
    navigate("/author/personal-profile");
  };

  return (
    <div style={{ padding: "20px", display: "flex", justifyContent: "center" }}>
      <div
        style={{
          backgroundColor: "white",
          width: "600px",
          padding: "30px",
          borderRadius: "8px",
          border: "1px solid #ddd",
        }}
      >
        <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
          Edit Profile
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "15px",
            marginBottom: "20px",
          }}
        >
          <div>
            <label>Họ và tên:</label>
            <input
              name="fullName"
              value={formData.fullName || ""}
              onChange={handleChange}
              style={inputStyle}
            />
          </div>
          <div>
            <label>Số điện thoại:</label>
            <input
              name="phone"
              value={formData.phone || ""}
              onChange={handleChange}
              style={inputStyle}
            />
          </div>
          <div>
            <label>Ngày sinh:</label>
            <input
              name="dob"
              value={formData.dob || ""}
              onChange={handleChange}
              style={inputStyle}
            />
          </div>
          <div>
            <label>Email:</label>
            <input
              name="email"
              value={formData.email || ""}
              onChange={handleChange}
              style={inputStyle}
            />
          </div>
          <div style={{ gridColumn: "span 2" }}>
            <label>Địa chỉ:</label>
            <input
              name="address"
              value={formData.address || ""}
              onChange={handleChange}
              style={inputStyle}
            />
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "center", gap: "20px" }}>
          <button onClick={handleSave} style={saveButtonStyle}>
            Update
          </button>
          <button
            onClick={() => navigate("/author/personal-profile")}
            style={cancelButtonStyle}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

const inputStyle = {
  width: "100%",
  padding: "10px",
  marginTop: "5px",
  borderRadius: "4px",
  border: "1px solid #ccc",
};
const saveButtonStyle = {
  backgroundColor: "#43B5AD",
  color: "white",
  border: "none",
  padding: "10px 40px",
  borderRadius: "20px",
  cursor: "pointer",
};
const cancelButtonStyle = {
  backgroundColor: "#666",
  color: "white",
  border: "none",
  padding: "10px 40px",
  borderRadius: "20px",
  cursor: "pointer",
};

export default EditProfile;
