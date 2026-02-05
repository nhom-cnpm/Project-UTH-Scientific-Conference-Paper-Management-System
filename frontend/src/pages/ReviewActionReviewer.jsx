import React, { useState } from "react";
import COIConfirmModal from "../components/COIConfirmModal"; // Import modal vừa tạo

const ReviewAction = () => {
  // Thêm state để theo dõi việc mở modal COI
  const [isCOIOpen, setIsCOIOpen] = useState(false);

  return (
    <div className="max-w-3xl mx-auto space-y-6 relative">
      <h2 className="text-center text-xl font-bold">Review Action</h2>

      {/* Nội dung thông tin bài báo (giữ nguyên như cũ) */}
      <div className="space-y-4 text-gray-800">
        <p>
          <strong>• Paper Title:</strong> Hệ thống giao thông AI
        </p>
        <p>
          <strong>• Conference:</strong> UTH-COMFMS
        </p>
        <p>
          <strong>• Deadline:</strong> 20/03/26
        </p>
        <p>
          <strong>• Abstract:</strong> Hệ thống giao thông AI ứng dụng trí tuệ
          nhân tạo...
        </p>
      </div>

      <div className="flex justify-center gap-20 py-4">
        <button className="text-blue-600 underline">View Paper Detail</button>
        <button className="text-blue-600 underline">Download PDF</button>
      </div>

      {/* Các nút hành động */}
      <div className="flex justify-center gap-4">
        <button className="bg-[#4ADE80] text-white px-6 py-2 rounded-xl font-bold shadow-md">
          Accept Review
        </button>
        <button className="bg-[#FF4D4D] text-white px-6 py-2 rounded-xl font-bold shadow-md">
          Decline Review
        </button>

        {/* Nút Declare COI: Thêm sự kiện onClick để mở modal */}
        <button
          onClick={() => setIsCOIOpen(true)}
          className="bg-[#FF9F43] text-white px-6 py-2 rounded-xl font-bold shadow-md hover:bg-orange-600 transition-colors"
        >
          Declare COI
        </button>
      </div>

      {/* Hiển thị Modal nếu isCOIOpen là true */}
      {isCOIOpen && <COIConfirmModal onClose={() => setIsCOIOpen(false)} />}
    </div>
  );
};

export default ReviewActionReviewer;
