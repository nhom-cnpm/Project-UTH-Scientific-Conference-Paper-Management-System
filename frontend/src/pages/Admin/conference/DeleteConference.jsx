import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { conferenceApi } from "../../../services/conferenceApi";

const DeleteConference = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const handleDelete = async () => {
    await conferenceApi.deleteConference(id);
    alert("Đã xóa hội nghị!");
    navigate("/conference-manage");
  };

  return (
    <div className="delete-container">
      <h2>Xác nhận xóa hội nghị #{id}?</h2>
      <button onClick={handleDelete} className="btn-delete">Xóa ngay</button>
      <button onClick={() => navigate("/conference-manage")}>Quay lại</button>
    </div>
  );
};
export default DeleteConference;