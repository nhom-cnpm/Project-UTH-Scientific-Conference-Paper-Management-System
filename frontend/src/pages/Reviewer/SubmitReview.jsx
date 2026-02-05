import React, { useState } from "react";
import ConfirmModal from "../../components/ConfirmModal"; // Sẽ tạo ở bước 3

const SubmitReview = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <h2 className="text-center text-xl font-bold">Review</h2>

      <div className="space-y-2">
        <label className="block font-medium">Overall Evaluation</label>
        <textarea
          placeholder="Write general comments"
          className="w-full border border-gray-300 p-3 rounded h-12 focus:outline-none focus:ring-1 focus:ring-teal-500"
        />
      </div>

      <div className="space-y-2">
        <label className="block font-medium">
          Strengths and weaknesses of the essay
        </label>
        <textarea
          placeholder="Write down the strengths and weaknesses of the essay"
          className="w-full border border-gray-300 p-3 rounded h-12 focus:outline-none focus:ring-1 focus:ring-teal-500"
        />
      </div>

      <div className="space-y-2">
        <label className="block font-medium">Overall score</label>
        <input
          type="text"
          placeholder="The rating scale is from 1 to 5."
          className="w-full border border-gray-300 p-3 rounded focus:outline-none focus:ring-1 focus:ring-teal-500"
        />
      </div>

      <div className="flex justify-center pt-10">
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-[#FF5F5F] text-white px-8 py-2 rounded-xl font-bold shadow-md hover:bg-red-500 transition-colors"
        >
          Submit Review
        </button>
      </div>

      {/* Modal xác nhận */}
      {isModalOpen && <ConfirmModal onClose={() => setIsModalOpen(false)} />}
    </div>
  );
};

export default SubmitReview;
