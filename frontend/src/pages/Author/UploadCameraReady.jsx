import React from "react";
import { useNavigate, useLocation } from "react-router-dom"; // Thêm useLocation

const UploadCameraReady = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Nhận dữ liệu bài viết từ trang trước truyền sang
  const paper = location.state?.paperData || { id: "Unknown" };

  // Hàm tạo thông báo lưu vào localStorage
  const createSystemNotification = (message) => {
    const savedNoti =
      JSON.parse(localStorage.getItem("authorNotifications")) || [];
    const newNoti = {
      message: message,
      date:
        new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
    };
    localStorage.setItem(
      "authorNotifications",
      JSON.stringify([newNoti, ...savedNoti]),
    );
  };

  const handleUpload = () => {
    // 1. Logic xử lý upload thực tế
    alert(`File for Paper ${paper.id} uploaded successfully!`);

    // 2. GỬI THÔNG BÁO VỀ HỆ THỐNG
    // Sử dụng dấu backtick để chèn ID động
    createSystemNotification(
      `You have successfully uploaded the Camera-ready version for Paper`,
    );

    // 3. Quay lại trang My Submission
    navigate("/author");
  };

  return (
    <div style={{ padding: "20px", maxWidth: "900px" }}>
      {/* Nút quay lại */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          marginBottom: "30px",
          cursor: "pointer",
          color: "#666",
        }}
        onClick={() => navigate(-1)}
      >
        <span style={{ fontSize: "24px", marginRight: "10px" }}>←</span>
        <span style={{ fontSize: "24px" }}>Back</span>
      </div>

      <h2 style={{ marginBottom: "20px" }}>Upload Camera-ready</h2>

      <div style={{ marginBottom: "30px", lineHeight: "1.5" }}>
        <p style={{ fontWeight: "500", margin: 0 }}>
          Congratulations! Your paper (ID: {paper.id}) has been accepted.
        </p>
        <p>
          Please upload the final camera-ready version (PDF) of your paper
          suitable for publication.
        </p>
      </div>

      <div
        style={{
          border: "1px solid #ddd",
          borderRadius: "4px",
          padding: "40px",
          backgroundColor: "white",
        }}
      >
        <p style={{ color: "#999", fontStyle: "italic", marginBottom: "30px" }}>
          Ensure your PDF meets the formatting and quality standard for
          publication
        </p>

        <div style={{ display: "flex", gap: "40px", alignItems: "center" }}>
          <div
            style={{
              flex: 1,
              height: "250px",
              border: "1px solid #eee",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <div style={{ textAlign: "center", color: "#ccc" }}>
              <span style={{ fontSize: "80px" }}>☁️</span>
              <div style={{ fontSize: "40px", marginTop: "-20px" }}>↑</div>
            </div>
          </div>

          <div style={{ width: "250px", fontSize: "16px", lineHeight: "2.5" }}>
            <div>
              Accpetable format: <strong>PDF</strong>
            </div>
            <div>
              Maximum file size: <strong>20MB</strong>
            </div>
          </div>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "40px",
          }}
        >
          <button onClick={handleUpload} style={uploadButtonStyle}>
            Upload
          </button>
        </div>
      </div>
    </div>
  );
};

const uploadButtonStyle = {
  backgroundColor: "#0052ff",
  color: "white",
  border: "none",
  padding: "10px 60px",
  borderRadius: "4px",
  fontSize: "18px",
  fontWeight: "500",
  cursor: "pointer",
};

export default UploadCameraReady;
