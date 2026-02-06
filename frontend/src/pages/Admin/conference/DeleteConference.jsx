import React, { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { conferenceApi } from "../../../services/conferenceApi";

const DeleteConference = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const deleteConference = async () => {
      try {
        await conferenceApi.deleteConference(id);
        alert("✅ Đã xóa hội nghị!");
        navigate("/admin/conference");
      } catch (error) {
        alert("❌ Xóa thất bại!");
        navigate("/admin/conference");
      }
    };

    deleteConference();
  }, [id, navigate]);

  return (
    <div style={{ padding: 20 }}>
      <h3>Đang xóa hội nghị #{id}...</h3>
    </div>
  );
};

export default DeleteConference;
