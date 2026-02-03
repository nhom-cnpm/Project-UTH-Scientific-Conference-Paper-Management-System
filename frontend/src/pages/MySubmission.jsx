import React from "react";

const MySubmission = () => {
  return (
    <div style={{ flex: 1, padding: "40px" }}>
      {/* Button Submit */}
      <button
        style={{
          backgroundColor: "#4f46e5",
          color: "white",
          padding: "10px 20px",
          borderRadius: "8px",
          border: "none",
          display: "flex",
          alignItems: "center",
          cursor: "pointer",
          marginBottom: "30px",
        }}
      >
        <span style={{ fontSize: "20px", marginRight: "8px" }}>+</span>
        Submit new articles
      </button>

      <h3>List of your articles</h3>

      {/* Table Area */}
      <div
        style={{
          backgroundColor: "white",
          borderRadius: "12px",
          overflow: "hidden",
          boxShadow: "0 2px 10px rgba(0,0,0,0.05)",
        }}
      >
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead style={{ backgroundColor: "#eeeeee" }}>
            <tr>
              <th style={{ textAlign: "left", padding: "15px" }}>
                Title of the article
              </th>
              <th style={{ textAlign: "left", padding: "15px" }}>Topic</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td
                colSpan="2"
                style={{
                  textAlign: "center",
                  padding: "50px",
                  color: "#666",
                  fontStyle: "italic",
                }}
              >
                No entries have been submitted yet.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MySubmission;
