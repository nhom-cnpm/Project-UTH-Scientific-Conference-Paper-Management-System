import React, { useState } from "react";
import COIFinalConfirmModal from "../components/COIFinalConfirmModal"; // Import modal mới

const DeclareCOIDetailsReviewer = () => {
  const [isFinalModalOpen, setIsFinalModalOpen] = useState(false);

  const coiTypes = [
    "Same affiliation as the authors",
    "Recent collaboration with the authors",
    "Personal relationship",
    "Financial interest",
    "Other:",
  ];

  return (
    <div className="max-w-3xl mx-auto relative">
      <h2 className="text-center text-xl font-bold mb-12 uppercase tracking-tight">
        Declare COI – Details
      </h2>

      <div className="space-y-6 ml-10">
        <h3 className="text-xl font-bold mb-4">
          Type of Conflict of Interest:
        </h3>

        {coiTypes.map((type) => (
          <div key={type} className="flex items-start gap-4">
            <input
              type="radio"
              name="coiType"
              id={type}
              className="mt-1.5 w-4 h-4 cursor-pointer accent-red-500"
            />
            <label htmlFor={type} className="text-lg cursor-pointer">
              {type}
            </label>
          </div>
        ))}

        <div className="ml-8">
          <textarea
            placeholder="Write details"
            className="w-full border border-gray-300 p-4 rounded h-32 focus:outline-none focus:ring-1 focus:ring-red-400 shadow-sm"
          ></textarea>
        </div>
      </div>

      <div className="flex justify-center mt-12">
        <button
          onClick={() => setIsFinalModalOpen(true)} // Mở modal khi bấm submit
          className="bg-[#FF5F5F] text-white px-14 py-2 rounded-xl font-bold shadow-md hover:bg-red-600 transition-colors"
        >
          Submit
        </button>
      </div>

      {/* Render Modal xác nhận cuối cùng */}
      {isFinalModalOpen && (
        <COIFinalConfirmModal onClose={() => setIsFinalModalOpen(false)} />
      )}
    </div>
  );
};

export default DeclareCOIDetailsReviewer;
