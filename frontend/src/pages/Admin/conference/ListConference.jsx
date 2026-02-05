import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { conferenceApi } from "../../../services/conferenceApi";

const ListConference = () => {
  const [conferences, setConferences] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    conferenceApi.getAll().then(setConferences);
  }, []);

  return (
    <div className="list-conference-container">
      <div className="list-header">
        <h2>Danh sách hội nghị</h2>
        <button onClick={() => navigate("/conference-manage/conference/create")}>
          + Tạo hội nghị
        </button>
      </div>
      <table className="conference-table">
        <thead>
          <tr>
            <th>Tên</th>
            <th>Thời gian</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {conferences.map((c) => (
            <tr key={c.id}>
              <td>{c.name}</td>
              <td>{c.startDate} - {c.endDate}</td>
              <td>
                <button onClick={() => navigate(`/conference-manage/conference/update/${c.id}`)}>Sửa</button>
                <button onClick={() => navigate(`/conference-manage/conference/delete/${c.id}`)}>Xoá</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
export default ListConference;