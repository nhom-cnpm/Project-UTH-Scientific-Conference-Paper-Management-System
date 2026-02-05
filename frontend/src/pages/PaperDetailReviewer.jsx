import React, { useState } from "react";

export default function PaperDetailReviewer({
  paper,
  onBack,
  actionButtonStyle,
}) {
  const [isReviewing, setIsReviewing] = useState(false);
  if (!paper) {
    return null;
  }
  //Giao diện review form
  if (isReviewing) {
    return (
      <div
        style={{
          backgroundColor: "white",
          padding: "30px",
          borderRadius: "12px",
        }}
      >
        <button
          onClick={() => setIsReviewing(false)}
          style={{
            background: "none",
            border: "none",
            color: "#4338ca",
            cursor: "pointer",
            fontWeight: "bold",
            marginBottom: "20px",
          }}
        >
          ← Back to Detail
        </button>
        <h2
          style={{
            textAlign: "center",
            fontSize: "24px",
            fontWeight: "bold",
            marginBottom: "40px",
          }}
        >
          Review
        </h2>
        <div style={{ maxWidth: "800px", margin: "0 auto" }}>
          <p style={{ fontWeight: "bold", marginBottom: "5px" }}>
            Overall Evaluation
          </p>
          <textarea
            placeholder="Write general comments"
            style={{
              width: "100%",
              height: "100px",
              marginBottom: "20px",
              padding: "10px",
            }}
          />

          <p style={{ fontWeight: "bold", marginBottom: "5px" }}>
            Strengths and weaknesses of the essay
          </p>
          <textarea
            placeholder="Write down the strengths and weaknesses of the essay"
            style={{
              width: "100%",
              height: "100px",
              marginBottom: "20px",
              padding: "10px",
            }}
          />

          <p style={{ fontWeight: "bold", marginBottom: "5px" }}>
            Overall score
          </p>
          <input
            type="text"
            placeholder="The rating scale is from 1 to 5."
            style={{ width: "100%", padding: "10px", marginBottom: "30px" }}
          />

          <div style={{ textAlign: "center" }}>
            <button
              onClick={() => {
                alert("Submit Success!");
                onBack();
              }}
              style={actionButtonStyle("#FF5F5F")}
            >
              Submit Review
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
      }}
    >
      {/* Nút Back */}
      <button
        onClick={onBack}
        style={{
          background: "none",
          border: "none",
          color: "#4338ca",
          cursor: "pointer",
          fontWeight: "bold",
          marginBottom: "20px",
        }}
      >
        ← Back
      </button>

      <h2
        style={{
          fontSize: "24px",
          fontWeight: "bold",
          textAlign: "center",
          marginBottom: "30px",
        }}
      >
        Paper Detail
      </h2>

      <div
        style={{
          maxWidth: "800px",
          margin: "0 auto",
          fontSize: "16px",
          lineHeight: "2",
        }}
      >
        {/* Thông tin bài báo */}
        <p>
          <strong>• Paper ID:</strong> {paper.paperId}
        </p>
        <p>
          <strong>• Paper Title:</strong> {paper.title}
        </p>
        <p>
          <strong>• Conference:</strong> {paper.conference}
        </p>
        <p>
          <strong>• Track/Topic:</strong> {paper.track}
        </p>
        <p>
          <strong>• Submission Date:</strong> {paper.submissionDate}
        </p>
        <p>
          <strong>• Review Deadline:</strong> {paper.deadline}
        </p>
        <p>
          <strong>• Authors:</strong> {paper.authors}
        </p>

        <div style={{ textAlign: "right", margin: "10px 0" }}>
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

        {/* Khung Abstract */}
        <div style={{ border: "1px solid #333", marginTop: "10px" }}>
          <div
            style={{
              backgroundColor: "#E8E8E8",
              padding: "5px 15px",
              fontWeight: "bold",
              borderBottom: "1px solid #333",
            }}
          >
            Abstract
          </div>
          <div style={{ padding: "15px", textAlign: "justify" }}>
            {paper.abstract}
          </div>
        </div>

        {/* Nút Review màu hồng */}
        <div style={{ textAlign: "center", marginTop: "30px" }}>
          <button
            onClick={() => setIsReviewing(true)}
            style={actionButtonStyle("#FF6B6B")}
          >
            Review
          </button>
        </div>
      </div>
    </div>
  );
}
