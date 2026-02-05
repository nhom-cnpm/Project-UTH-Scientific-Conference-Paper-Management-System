import React from "react";
import SidebarAuthor from "../components/SidebarAuthor";
import "../styles/PersonalProfile.css";

const PersonalProfile = () => {
  return (
    <div className="profile-dashboard">
      <SidebarGuest />

      <div className="profile-main">
        <header className="profile-header">
          <div className="user-dropdown">
            <div className="avatar-mini"></div>
            <span>Nguyen Van A</span>
            <i className="arrow-down"></i>
          </div>
        </header>

        <div className="profile-content">
          {/* Phần Information problem */}
          <section className="info-section">
            <h3 className="section-title">Information problem</h3>
            <div className="info-card display-flex">
              <div className="profile-avatar-large">
                {/* Icon người dùng lớn */}
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1"
                >
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <div className="info-details">
                <p>
                  <strong>Họ và tên:</strong> Nguyễn Văn A
                </p>
                <p>
                  <strong>Số CCCD:</strong> 0739446149
                </p>
                <p>
                  <strong>Ngày sinh:</strong> 03/07/2004
                </p>
                <p>
                  <strong>Trình độ học vấn:</strong> Đại học
                </p>
              </div>
            </div>
          </section>

          {/* Phần Personal information */}
          <section className="info-section">
            <h3 className="section-title">Personal information</h3>
            <div className="info-card">
              <div className="info-grid">
                <p>
                  <strong>Giới tính:</strong> Nam
                </p>
                <p>
                  <strong>Dân tộc:</strong> Kinh
                </p>
                <p>
                  <strong>Ngày vào đoàn:</strong> <em>Chưa cập nhật</em>
                </p>
                <p>
                  <strong>Ngày vào đảng:</strong> <em>Chưa cập nhật</em>
                </p>
                <p>
                  <strong>Số điện thoại:</strong> 0113146779
                </p>
                <p>
                  <strong>Email cá nhân:</strong> nguyenvana@gmail.com
                </p>
                <p>
                  <strong>Địa chỉ thường trú:</strong> P.25, Bình Thạnh
                </p>
              </div>
            </div>
          </section>

          <div className="action-area">
            <button className="btn-update">Update personal information</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PersonalProfile;
