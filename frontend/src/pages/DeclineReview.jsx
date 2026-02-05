import React, { useState } from "react";
import DeclineConfirmModal from "../components/DeclineConfirmModal";

const DeclineReview = () => {
  // State để quản lý việc hiển thị Modal (mặc định là false - đóng)
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Hàm xử lý khi nhấn nút Submit Reason
  const handleSubmitClick = () => {
    setIsModalOpen(true); // Mở modal lên
  };

  return (
    <div className="max-w-3xl mx-auto relative">
      <h2 className="text-center text-xl font-bold mb-12">Decline review</h2>

      <div className="space-y-6 ml-10">
        {[
          "Paper Not in My Field",
          "Lack of Expertise",
          "Time Constraints",
          "Conflict of Interest",
          "Other:",
        ].map((reason) => (
          <div key={reason} className="flex items-start gap-4">
            <input
              type="radio"
              name="declineReason"
              id={reason}
              className="mt-1.5 w-4 h-4 cursor-pointer"
            />
            <label htmlFor={reason} className="text-lg cursor-pointer">
              {reason}
            </label>
          </div>
        ))}
        <div className="ml-8">
          <textarea
            placeholder="Write another reason....."
            className="w-full border border-gray-300 p-4 rounded h-32 focus:outline-none focus:ring-1 focus:ring-red-400"
          ></textarea>
        </div>
      </div>

      <div className="flex justify-center mt-12">
        <button
          onClick={handleSubmitClick} // Gọi hàm mở modal khi click
          className="bg-[#FF5F5F] text-white px-10 py-2 rounded-xl font-bold shadow-md hover:bg-red-600 transition-colors"
        >
          Submit Reason
        </button>
      </div>

      {/* Nếu isModalOpen là true thì render Modal */}
      {isModalOpen && (
        <DeclineConfirmModal onClose={() => setIsModalOpen(false)} />
      )}
    </div>
  );
};

export default DeclineReview;
