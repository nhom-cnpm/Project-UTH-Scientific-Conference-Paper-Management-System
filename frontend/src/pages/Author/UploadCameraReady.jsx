import React from "react";
import { useNavigate } from "react-router-dom";

const UploadCameraReady = () => {
  const navigate = useNavigate();

  const handleUpload = () => {
    // 1. Bạn có thể thêm logic xử lý file thực tế ở đây
    alert("File uploaded successfully!");

    // 2. Sau khi upload xong, quay lại trang My Submission
    navigate("/author");
  };

  return (
    <div style={{ padding: "20px", maxWidth: "900px" }}>
      {/* Nút quay lại thủ công */}
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

      <h2 style={{ marginBottom: "20px" }}>Upload Camera-ready</h2>

      <div style={{ marginBottom: "30px", lineHeight: "1.5" }}>
        <p style={{ fontWeight: "500", margin: 0 }}>
          Congratulations! Your paper has been accepted.
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
          {/* Vùng icon upload */}
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

          {/* Thông số file */}
          <div style={{ width: "250px", fontSize: "16px", lineHeight: "2.5" }}>
            <div>
              Accpetable format: <strong>PDF</strong>
            </div>
            <div>
              Maximum file size: <strong>20MB</strong>
            </div>
          </div>
        </div>

        {/* NÚT UPLOAD XỬ LÝ ĐIỀU HƯỚNG */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "40px",
          }}
        >
          <button
            onClick={handleUpload}
            style={{
              backgroundColor: "#0052ff",
              color: "white",
              border: "none",
              padding: "10px 60px",
              borderRadius: "4px",
              fontSize: "18px",
              fontWeight: "500",
              cursor: "pointer",
            }}
          >
            Upload
          </button>
        </div>
      </div>
    </div>
  );
};

export default UploadCameraReady;
