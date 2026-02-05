import React from "react";
import { useNavigate } from "react-router-dom"; // Thêm useNavigate

const COIConfirmModal = ({ onClose }) => {
  const navigate = useNavigate();

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50 px-4">
      <div className="bg-white rounded-sm shadow-2xl p-12 max-w-xl w-full border border-gray-100">
        <h3 className="text-3xl text-center leading-tight mb-16 font-bold text-gray-900">
          Do you have a Conflict of Interest with this paper?
        </h3>

        <div className="flex justify-around items-center px-10">
          <button
            onClick={() => {
              onClose();
              navigate("/declare-coi-details"); // Chuyển hướng khi chọn Yes
            }}
            className="text-3xl font-bold hover:text-teal-600 transition-colors"
          >
            Yes
          </button>
          <button
            onClick={onClose}
            className="text-3xl font-bold hover:text-red-600 transition-colors"
          >
            No
          </button>
        </div>
      </div>
    </div>
  );
};

export default COIConfirmModal;
