import React from "react";
import { useNavigate } from "react-router-dom";

const COIFinalConfirmModal = ({ onClose }) => {
  const navigate = useNavigate();

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50 px-4">
      {/* Container trắng */}
      <div className="bg-white rounded-sm shadow-2xl p-10 max-w-2xl w-full border border-gray-100 animate-in fade-in zoom-in duration-200">
        {/* Thông báo cảnh báo */}
        <h3 className="text-3xl text-center leading-snug mb-20 font-bold text-gray-900 px-6">
          After submitting COI, you will not be able to review this paper
        </h3>

        {/* Nút bấm điều hướng */}
        <div className="flex justify-around items-center px-4">
          <button
            onClick={() => {
              // Xử lý gửi dữ liệu ở đây nếu cần
              navigate("/assigned"); // Quay về trang View Assigned Papers
            }}
            className="text-3xl font-bold text-gray-900 hover:text-teal-600 transition-colors"
          >
            Submit COI
          </button>
          <button
            onClick={onClose} // Đóng modal quay về trang Details
            className="text-3xl font-bold text-gray-900 hover:text-red-600 transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default COIFinalConfirmModal;
