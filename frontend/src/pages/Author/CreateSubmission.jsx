import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const CreateSubmission = () => {
  const navigate = useNavigate();

  // 1. Tạo state để lưu trữ thông tin form
  const [paperTitle, setPaperTitle] = useState("");
  const [topic, setTopic] = useState("");

  const handleSubmit = () => {
    if (!paperTitle || !topic) {
      alert("Please fill in Paper Title and Topic!");
      return;
    }

    // 2. Lấy danh sách hiện có từ localStorage (hoặc mảng trống nếu chưa có)
    const existingSubmissions = JSON.parse(
      localStorage.getItem("submissions"),
    ) || [
      { id: 1, title: "Hệ thống giao thông AI", topic: "Trí tuệ nhân tạo" },
      {
        id: 2,
        title: "Xây dựng hệ thống quản lý thư viện thông minh",
        topic: "Trí tuệ nhân tạo",
      },
    ];

    // 3. Thêm bài mới vào danh sách
    const newSubmission = {
      id: Date.now(), // Tạo ID duy nhất
      title: paperTitle,
      topic: topic,
    };

    const updatedList = [...existingSubmissions, newSubmission];

    // 4. Lưu lại vào localStorage và chuyển trang
    localStorage.setItem("submissions", JSON.stringify(updatedList));

    alert("Submitted successfully!");
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
        <span style={{ fontSize: "24px" }}>→</span>
      </div>

      <h2 style={{ textAlign: "center", marginBottom: "10px" }}>
        Create Submission
      </h2>
      <p style={{ textAlign: "center", marginBottom: "40px", color: "#333" }}>
        Please fill out the form below to submit your paper to the conference.
      </p>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "25px",
          paddingLeft: "50px",
        }}
      >
        {/* Input Title */}
        <div style={{ display: "flex", alignItems: "center" }}>
          <label style={{ width: "150px", fontSize: "18px" }}>
            Paper Title
          </label>
          <input
            type="text"
            value={paperTitle}
            onChange={(e) => setPaperTitle(e.target.value)} // Cập nhật state
            placeholder="Enter your paper title"
            style={{
              flex: 1,
              padding: "10px",
              border: "1px solid #ddd",
              borderRadius: "4px",
            }}
          />
        </div>

        {/* Input Topic */}
        <div style={{ display: "flex", alignItems: "center" }}>
          <label style={{ width: "150px", fontSize: "18px" }}>
            Topic/Track
          </label>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)} // Cập nhật state
            placeholder="Enter topic/track"
            style={{
              flex: 1,
              padding: "10px",
              border: "1px solid #ddd",
              borderRadius: "4px",
            }}
          />
        </div>

        {/* Các trường khác giữ nguyên giao diện như code cũ của bạn */}
        <div style={{ display: "flex", alignItems: "center" }}>
          <label style={{ width: "150px", fontSize: "18px" }}>Authors</label>
          <input
            type="text"
            placeholder="Enter your first and last name."
            style={{
              flex: 1,
              padding: "10px",
              border: "1px solid #ddd",
              borderRadius: "4px",
            }}
          />
        </div>

        <div style={{ fontSize: "18px" }}>Conference: UTH-COMFMS</div>

        <div>
          <label
            style={{ display: "block", fontSize: "18px", marginBottom: "10px" }}
          >
            Abstrack
          </label>
          <textarea
            placeholder="Enter a concise abstrack of your paper"
            style={{
              width: "100%",
              height: "120px",
              padding: "15px",
              border: "1px solid #ddd",
              borderRadius: "4px",
            }}
          />
        </div>

        {/* Vùng Upload PDF */}
        <div>
          <label
            style={{ display: "block", fontSize: "18px", marginBottom: "10px" }}
          >
            Upload paper (PDF)
          </label>
          <div
            style={{
              border: "1px solid #ddd",
              padding: "30px",
              textAlign: "center",
              borderRadius: "4px",
            }}
          >
            <div style={{ color: "#999", marginBottom: "10px" }}>
              ☁️ Drag and drop your PDF file here, or click to select a file
            </div>
            <div style={{ color: "#ccc", fontSize: "14px" }}>
              Accpetable format: PDF, Maximum file size: 20MB
            </div>
          </div>
        </div>

        {/* Nút Submit xử lý điều hướng */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "20px",
          }}
        >
          <button
            onClick={handleSubmit}
            style={{
              backgroundColor: "#0052ff",
              color: "white",
              border: "none",
              padding: "12px 80px",
              borderRadius: "4px",
              fontSize: "18px",
              cursor: "pointer",
            }}
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateSubmission;
