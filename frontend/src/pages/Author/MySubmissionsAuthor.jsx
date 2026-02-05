<<<<<<< HEAD
// import React, { use } from "react";
=======
import React, { useEffect, useState } from "react";
>>>>>>> 1541c147e4d261a71268bf77a109a26716d1753b
import { useNavigate } from "react-router-dom";

import React, { useEffect, useState} from "react";

const MySubmissionsAuthor = () => {
  const navigate = useNavigate();
  const [submissions, setSubmissions] = useState([]);

  useEffect(() => {
    const defaultData = [
      { id: 1, title: "Hệ thống giao thông AI", topic: "Trí tuệ nhân tạo" },
      {
        id: 2,
        title: "Xây dựng hệ thống quản lý thư viện thông minh",
        topic: "Trí tuệ nhân tạo",
      },
    ];
    const savedData = JSON.parse(localStorage.getItem("submissions"));
    if (savedData && savedData.length > 0) {
      setSubmissions(savedData);
    } else {
      setSubmissions(defaultData);
      localStorage.setItem("submissions", JSON.stringify(defaultData));
    }
  }, []);

  // const [submissions, setSubmissions] = useState([]);
  // const [loading, setLoading] = useState(true);
  // useEffect(() => {
  //   fetch("http://localhost:8000/submission/accepted/")
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setSubmissions(data);
  //       setLoading(false);
  //     })
  //     .catch((err) => {
  //       console.error("API error:", err);
  //       setLoading(false);
  //     });
  // }, []);



  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        width: "100%",
        alignItems: "center",
      }}
    >
      {/* Nút Submit */}
      <div style={{ width: "100%", textAlign: "left", marginBottom: "25px" }}>
        <button
          onClick={() => navigate("/author/create-submission")}
          style={{
            backgroundColor: "#5865f2",
            color: "white",
            border: "none",
            padding: "10px 25px",
            borderRadius: "15px",
            cursor: "pointer",
            fontWeight: "500",
          }}
        >
          + Submit new articles!
        </button>
      </div>

      <h2
        style={{
          width: "100%",
          textAlign: "left",
          marginBottom: "20px",
          fontWeight: "500",
          fontSize: "22px",
        }}
      >
        List of your articles
      </h2>

      {/* BẢNG ĐÃ CHỈNH MÀU XANH NGỌC */}
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ backgroundColor: "#43B5AD" }}>
            {" "}
            {/* Màu xanh ngọc cho dòng tiêu đề */}
            <th
              style={{
                padding: "15px",
                border: "1px solid #ddd",
                textAlign: "left",
                fontWeight: "normal",
                color: "white",
                backgroundColor: "#43B5AD", // Cố định màu xanh ngọc ở đây
              }}
            >
              Title of the article
            </th>
            <th
              style={{
                padding: "15px",
                border: "1px solid #ddd",
                textAlign: "left",
                fontWeight: "normal",
                width: "30%",
                color: "white",
                backgroundColor: "#43B5AD", // Cố định màu xanh ngọc ở đây
              }}
            >
              Topic
            </th>
          </tr>
        </thead>
        <tbody>
          {submissions.map((item, index) => (
            <tr key={item.id} style={{ borderBottom: "1px solid #eee" }}>
              <td style={{ padding: "15px", border: "1px solid #eee" }}>
                {index + 1}. {item.title}
              </td>
              <td style={{ padding: "15px", border: "1px solid #eee" }}>
                {item.topic}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Cụm nút đỏ cam phía dưới */}
      <div
        style={{
          marginTop: "60px",
          width: "100%",
          display: "flex",
          gap: "100px",
          justifyContent: "center",
        }}
      >
        <button
          onClick={() => navigate("/author/submission-detail")}
          style={{
            backgroundColor: "#ff6b6b",
            color: "white",
            border: "none",
            padding: "12px 70px",
            borderRadius: "30px",
            fontSize: "17px",
            fontWeight: "bold",
            cursor: "pointer",
            boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
          }}
        >
          Submission Detail
        </button>
        <button
          onClick={() => navigate("/author/upload-camera-ready")}
          style={{
            backgroundColor: "#ff6b6b",
            color: "white",
            border: "none",
            padding: "12px 40px",
            borderRadius: "25px",
            fontSize: "16px",
            fontWeight: "bold",
            cursor: "pointer",
            boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
          }}
        >
          Upload camera-ready
        </button>
      </div>
    </div>
  );
};

export default MySubmissionsAuthor;
