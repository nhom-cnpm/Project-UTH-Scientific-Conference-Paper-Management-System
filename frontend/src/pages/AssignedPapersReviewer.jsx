import React, { useState } from "react";
import PaperDetailReviewer from "./PaperDetailReviewer";
import DeclineReview from "./DeclineReview";
import DeclareCOIDetailsReviewer from "./DeclareCOIDetailsReviewer";

const AssignedPapersReviewer = () => {
  // Bổ sung State để quản lý bài báo đang được chọn
  const [selectedPaper, setSelectedPaper] = useState(null);
  const [showFullDetail, setShowFullDetail] = useState(false);
  const [showDeclineForm, setShowDeclineForm] = useState(false);
  const [showCOIForm, setShowCOIForm] = useState(false);

  const papers = [
    {
      id: 1,
      paperId: "P-0123",
      title: "Hệ thống giao thông AI",
      conference: "UTH-COMFMS",
      track: "Artificial Intelligence",
      submissionDate: "10/02/2026",
      deadline: "20/03/26",
      status: "Declined",
      authors: "Nguyễn Văn A – UTH",
      abstract:
        "Hệ thống giao thông AI ứng dụng trí tuệ nhân tạo để phân tích dữ liệu giao thông và dự đoán tình trạng ùn tắc. Nghiên cứu nhằm hỗ trợ điều tiết giao thông hiệu quả, giảm kẹt xe và nâng cao an toàn giao thông đô thị.",
    },
    {
      id: 2,
      paperId: "P-0456",
      title: "Quản lý sự kiện trong trường",
      conference: "UTH-COMFMS",
      track: "Software Engineering",
      submissionDate: "12/02/2026",
      deadline: "COI",
      status: "COI",
      authors: "Trần Văn B – UTH",
      abstract:
        "Nghiên cứu về giải pháp số hóa quy trình quản lý sự kiện trong môi trường đại học nhằm tối ưu hóa việc đăng ký và theo dõi lịch trình.",
    },
    {
      id: 3,
      paperId: "P-0789",
      title: "Chăm sóc sức khoẻ thông minh",
      conference: "UTH-COMFMS",
      track: "Internet of Things",
      submissionDate: "15/02/2026",
      deadline: "COI",
      status: "Reviewed",
      authors: "Lê Thị C – UTH",
      abstract:
        "Ứng dụng cảm biến thông minh trong việc theo dõi sức khỏe bệnh nhân từ xa và cảnh báo sớm các dấu hiệu bất thường.",
    },
    {
      id: 4,
      paperId: "P-1011",
      title: "Giám sát y tế cộng đồng bằng AI",
      conference: "UTH-COMFMS",
      track: "Data Science",
      submissionDate: "18/02/2026",
      deadline: "27/03/26",
      status: "Pending",
      authors: "Phạm Văn D – UTH",
      abstract:
        "Phân tích dữ liệu y tế quy mô lớn bằng học máy để dự báo xu hướng dịch bệnh trong cộng đồng.",
    },
    {
      id: 5,
      paperId: "P-1213",
      title: "Hệ thống gia sư thông minh bằng AI",
      conference: "UTH-COMFMS",
      track: "Education Tech",
      submissionDate: "20/02/2026",
      deadline: "22/03/26",
      status: "Pending",
      authors: "Hoàng Thị E – UTH",
      abstract:
        "Xây dựng trợ lý học tập cá nhân hóa dựa trên AI giúp sinh viên cải thiện kết quả học tập thông qua lộ trình riêng biệt.",
    },
  ];

  const tableHeaderStyle = {
    backgroundColor: "#43B5AD",
    color: "white",
    padding: "15px 20px",
    textAlign: "center",
    fontSize: "15px",
    fontWeight: "600",
    border: "1px solid #fff",
  };

  const tableCellStyle = {
    padding: "25px 20px",
    fontSize: "14px",
    color: "#333",
    borderBottom: "1px solid #eee",
    borderRight: "1px solid #eee",
    textAlign: "center",
  };

  const actionButtonStyle = (color) => ({
    padding: "12px 25px",
    borderRadius: "10px",
    border: "none",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
    fontSize: "15px",
    backgroundColor: color,
  });

  // Điều hướng qua giao diện COI
  if (showCOIForm) {
    return (
      <DeclareCOIDetailsReviewer
        onBack={() => setShowCOIForm(false)}
        onSubmitSuccess={() => {
          alert("COI Declared Successfully!");
          setShowCOIForm(false);
          setSelectedPaper(null);
        }}
      />
    );
  }

  // --- ĐIỀU HƯỚNG QUA GIAO DIỆN TỪ CHỐI ---
  if (showDeclineForm) {
    return (
      <DeclineReview
        onBack={() => setShowDeclineForm(false)}
        onSubmitSuccess={() => {
          alert("Submitted Reason Successfully!");
          setShowDeclineForm(false);
          setSelectedPaper(null);
        }}
      />
    );
  }

  // --- Điều hướng qua Paper Detail ---
  if (showFullDetail && selectedPaper) {
    return (
      <PaperDetailReviewer
        paper={selectedPaper}
        onBack={() => setShowFullDetail(false)}
        actionButtonStyle={actionButtonStyle}
      />
    );
  }

  // --- GIAO DIỆN CHI TIẾT (Review Action) ---
  if (selectedPaper) {
    return (
      <div
        style={{
          backgroundColor: "white",
          padding: "30px",
          borderRadius: "12px",
        }}
      >
        <button
          onClick={() => setSelectedPaper(null)}
          style={{
            background: "none",
            border: "none",
            color: "#4338ca",
            cursor: "pointer",
            fontWeight: "bold",
            marginBottom: "20px",
          }}
        >
          ← Back to list
        </button>

        <h2
          style={{
            fontSize: "24px",
            fontWeight: "bold",
            textAlign: "center",
            marginBottom: "40px",
          }}
        >
          Review Action
        </h2>

        <div
          style={{
            maxWidth: "900px",
            margin: "0 auto",
            fontSize: "16px",
            lineHeight: "1.8",
          }}
        >
          <p>
            <strong>• Paper Title:</strong> {selectedPaper.title}
          </p>
          <p>
            <strong>• Conference:</strong> {selectedPaper.conference}
          </p>
          <p>
            <strong>• Deadline:</strong> {selectedPaper.deadline}
          </p>
          <p style={{ textAlign: "justify" }}>
            <strong>• Abstract:</strong> {selectedPaper.abstract}
          </p>

          <div
            style={{
              display: "flex",
              justifyContent: "center",
              gap: "60px",
              margin: "40px 0",
            }}
          >
            <span
              onClick={() => setShowFullDetail(true)}
              style={{
                color: "#4338ca",
                cursor: "pointer",
                textDecoration: "underline",
              }}
            >
              View Paper Detail
            </span>
            <span
              style={{
                color: "#4338ca",
                cursor: "pointer",
                textDecoration: "underline",
              }}
            >
              Download PDF
            </span>
          </div>

          <div
            style={{ display: "flex", justifyContent: "center", gap: "25px" }}
          >
            <button
              onClick={() => setShowFullDetail(true)}
              style={actionButtonStyle("#00E640")}
            >
              Accept Review
            </button>
            <button
              onClick={() => setShowDeclineForm(true)}
              style={actionButtonStyle("#FF0000")}
            >
              Decline Review
            </button>
            <button
              onClick={() => setShowCOIForm(true)}
              style={actionButtonStyle("#FF8C00")}
            >
              Declare COI
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        backgroundColor: "white",
        padding: "30px",
        borderRadius: "12px",
        boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          fontSize: "22px",
          marginBottom: "30px",
          fontWeight: "bold",
          textAlign: "center",
          color: "#2d3748",
        }}
      >
        View Assigned Papers
      </h2>
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          border: "1px solid #eee",
        }}
      >
        <thead>
          <tr>
            <th style={{ ...tableHeaderStyle, textAlign: "left" }}>
              Paper Title
            </th>
            <th style={tableHeaderStyle}>Conference</th>
            <th style={tableHeaderStyle}>Deadline</th>
            <th style={tableHeaderStyle}>Status</th>
            <th style={tableHeaderStyle}>Action</th>
          </tr>
        </thead>
        <tbody>
          {papers.map((paper) => (
            <tr key={paper.id} style={{ borderBottom: "1px solid #eee" }}>
              <td
                style={{
                  ...tableCellStyle,
                  textAlign: "left",
                  width: "35%",
                  fontWeight: "500",
                }}
              >
                {paper.title}
              </td>
              <td style={tableCellStyle}>{paper.conference}</td>
              <td style={tableCellStyle}>{paper.deadline}</td>
              <td
                style={{
                  ...tableCellStyle,
                  color: paper.status === "Declined" ? "#e53e3e" : "#333",
                }}
              >
                {paper.status}
              </td>
              <td style={tableCellStyle}>
                <button
                  onClick={() => setSelectedPaper(paper)}
                  style={{
                    color: "#4338ca",
                    background: "none",
                    border: "none",
                    cursor: "pointer",
                    fontWeight: "600",
                    fontSize: "14px",
                    textDecoration: "underline",
                  }}
                >
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AssignedPapersReviewer;
