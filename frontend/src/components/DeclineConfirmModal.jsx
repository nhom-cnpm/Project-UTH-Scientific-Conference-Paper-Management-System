import React from "react";

const DeclineConfirmModal = ({ onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50 px-4">
      {/* Container của Modal trắng */}
      <div className="bg-white rounded-sm shadow-2xl p-10 max-w-xl w-full border border-gray-100 relative animate-in fade-in zoom-in duration-200">
        {/* Nội dung thông báo */}
        <h3 className="text-2xl text-center leading-relaxed mb-16 font-medium text-gray-800 px-4">
          After submitting the reasons for rejection, the reviewer will no
          longer be able to consider this paper.
        </h3>

        {/* Hai nút lựa chọn */}
        <div className="flex justify-around items-center">
          <button
            onClick={() => {
              alert("Đã xác nhận từ chối!");
              onClose();
            }}
            className="text-2xl font-semibold text-gray-800 hover:text-red-600 transition-colors"
          >
            Sure
          </button>
          <button
            onClick={onClose} // Đóng modal khi nhấn Cancel
            className="text-2xl font-semibold text-gray-800 hover:text-blue-600 transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeclineConfirmModal;
