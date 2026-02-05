const ReviewAction = () => {
  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h2 className="text-center text-xl font-bold">Review Action</h2>
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
          nhân tạo để phân tích dữ liệu giao thông và dự đoán tình trạng ùn tắc.
          Nghiên cứu nhằm hỗ trợ điều tiết giao thông hiệu quả, giảm kẹt xe và
          nâng cao an toàn giao thông đô thị.
        </p>
      </div>

      <div className="flex justify-center gap-20 py-4">
        <button className="text-blue-600 underline">View Paper Detail</button>
        <button className="text-blue-600 underline">Download PDF</button>
      </div>

      <div className="flex justify-center gap-4">
        <button className="bg-green-500 text-white px-6 py-2 rounded-full font-bold">
          Accept Review
        </button>
        <button className="bg-red-600 text-white px-6 py-2 rounded-full font-bold">
          Decline Review
        </button>
        <button className="bg-orange-500 text-white px-6 py-2 rounded-full font-bold">
          Declare COI
        </button>
      </div>
    </div>
  );
};

export default ReviewAction;
