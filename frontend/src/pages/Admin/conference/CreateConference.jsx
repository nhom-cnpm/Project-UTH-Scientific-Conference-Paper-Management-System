import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { conferenceApi } from "../../../services/conferenceApi";
import "../../../styles/AdminQuanli.css";

const CreateConference = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    shortName: "", 
    location: "",
    startDate: "", 
    endDate: "", 
    description: "",
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await conferenceApi.createConference(formData);
      alert(" Tạo hội nghị thành công!");
      navigate("/admin");
    } catch (err) {
      alert(" Có lỗi xảy ra!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="conference-form-container">
      <h2>Tạo hội nghị mới</h2>
      <form onSubmit={handleSubmit} className="conference-form">
        <div className="form-group">
          <label>Tên hội nghị</label>
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Tên viết tắt</label>
          <input type="text" name="shortName" value={formData.shortName} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Địa điểm</label>
          <input type="text" name="location" value={formData.location} onChange={handleChange} />
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Ngày bắt đầu</label>
            <input type="date" name="startDate" value={formData.startDate} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Ngày kết thúc</label>
            <input type="date" name="endDate" value={formData.endDate} onChange={handleChange} required />
          </div>
        </div>
        <div className="form-group">
          <label>Mô tả</label>
          <textarea name="description" rows="4" value={formData.description} onChange={handleChange} />
        </div>
        <div className="form-actions">
           <button type="button" className="btn-secondary" onClick={() => navigate(-1)}>Huỷ</button>
           <button type="submit" className="btn-primary" disabled={loading}>
             {loading ? "Đang tạo..." : "Tạo hội nghị"}
           </button>
        </div>
      </form>
    </div>
  );
};

export default CreateConference;