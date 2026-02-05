import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { conferenceApi } from "../../../services/conferenceApi";

const UpdateConference = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", shortName: "", location: "", startDate: "", endDate: "", description: "" });

  useEffect(() => {
    conferenceApi.getConferenceById(id).then((data) => {
      if (data) setForm(data);
    });
  }, [id]);

  const handleSubmit = (e) => {
    e.preventDefault();
    conferenceApi.updateConference(id, form).then(() => {
      alert("Cập nhật thành công!");
      navigate("/conference-manage"); // Quay về trang index của quản lý
    });
  };

  return (
    <div className="conference-form-container">
      <h2>Sửa hội nghị</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" value={form.name} onChange={(e) => setForm({...form, name: e.target.value})} />
        {/* Tương tự cho các input khác... */}
        <button type="submit">Lưu lại</button>
        <button type="button" onClick={() => navigate("/conference-manage")}>Hủy</button>
      </form>
    </div>
  );
};
export default UpdateConference;