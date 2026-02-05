import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const PersonalProfile = () => {
  const navigate = useNavigate();
  const [profile, setProfile] = useState({});

  useEffect(() => {
    const savedProfile = JSON.parse(localStorage.getItem("authorProfile")) || {
      fullName: "Nguyễn Văn A",
      cccd: "0739446149",
      dob: "03/07/2004",
      education: "Đại học",
      gender: "Nam",
      ethnicity: "Kinh",
      joinUnion: "Chưa cập nhật",
      joinParty: "Chưa cập nhật",
      phone: "0113146779",
      email: "nguyenvana@gmail.com",
      address: "P.25, Bình Thạnh",
    };
    setProfile(savedProfile);
    if (!localStorage.getItem("authorProfile")) {
      localStorage.setItem("authorProfile", JSON.stringify(savedProfile));
    }
  }, []);

  return (
    <div style={{ padding: "20px", display: "flex", justifyContent: "center" }}>
      <div
        style={{
          backgroundColor: "#f9f9f9",
          width: "600px",
          padding: "30px",
          borderRadius: "8px",
        }}
      >
        {/* Information problem section */}
        <div
          style={{
            backgroundColor: "#e8eaf6",
            padding: "10px",
            fontWeight: "bold",
            marginBottom: "15px",
          }}
        >
          Information problem
        </div>
        <div style={{ display: "flex", gap: "20px", marginBottom: "30px" }}>
          <div
            style={{
              width: "120px",
              height: "120px",
              backgroundColor: "#43B5AD",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <span style={{ fontSize: "50px", color: "white" }}>👤</span>
          </div>
          <div style={{ lineHeight: "1.8" }}>
            Họ và tên: {profile.fullName} <br />
            Số CCCD: {profile.cccd} <br />
            Ngày sinh: {profile.dob} <br />
            Trình độ học vấn: {profile.education}
          </div>
        </div>

        {/* Personal information section */}
        <div
          style={{
            backgroundColor: "#e8eaf6",
            padding: "10px",
            fontWeight: "bold",
            marginBottom: "15px",
          }}
        >
          Personal information
        </div>
        <div
          style={{ lineHeight: "2", marginBottom: "30px", paddingLeft: "10px" }}
        >
          Giới tính: {profile.gender} <br />
          Dân tộc: {profile.ethnicity} <br />
          Ngày vào đoàn: {profile.joinUnion} <br />
          Ngày vào đảng: {profile.joinParty} <br />
          Số điện thoại: {profile.phone} <br />
          Email cá nhân: {profile.email} <br />
          Địa chỉ thường trú: {profile.address}
        </div>

        <div style={{ textAlign: "center" }}>
          <button
            onClick={() => navigate("/author/edit-profile")}
            style={{
              backgroundColor: "#5865f2",
              color: "white",
              border: "none",
              padding: "12px 30px",
              borderRadius: "25px",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            Update personal information
          </button>
        </div>
      </div>
    </div>
  );
};

export default PersonalProfile;
