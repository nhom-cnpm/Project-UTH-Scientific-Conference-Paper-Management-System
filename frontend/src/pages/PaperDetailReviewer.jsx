const PaperDetail = () => {
  const paperInfo = {
    id: "P-0123",
    title: "Hệ thống giao thông AI",
    conference: "UTH-COMFMS",
    track: "Artificial Intelligence",
    submissionDate: "10/02/2026",
    deadline: "20/03/2026",
    authors: "Nguyễn Văn A – UTH",
    abstract:
      "Hệ thống giao thông AI ứng dụng trí tuệ nhân tạo để phân tích dữ liệu giao thông và dự đoán tình trạng ùn tắc. Nghiên cứu nhằm hỗ trợ điều tiết giao thông hiệu quả, giảm kẹt xe và nâng cao an toàn giao thông đô thị.",
  };

  return (
    <div className="max-w-3xl mx-auto">
      <h2 className="text-center text-xl font-bold mb-6">Paper Detail</h2>
      <div className="space-y-4 mb-6">
        <p>
          <strong>• Paper ID:</strong> {paperInfo.id}
        </p>
        <p>
          <strong>• Paper Title:</strong> {paperInfo.title}
        </p>
        <p>
          <strong>• Conference:</strong> {paperInfo.conference}
        </p>
        <p>
          <strong>• Track/Topic:</strong> {paperInfo.track}
        </p>
        <p>
          <strong>• Submission Date:</strong> {paperInfo.submissionDate}
        </p>
        <p>
          <strong>• Review Deadline:</strong> {paperInfo.deadline}
        </p>
        <p>
          <strong>• Authors:</strong> {paperInfo.authors}
        </p>
      </div>

      <div className="flex justify-end mb-2">
        <button className="text-blue-600 text-sm hover:underline">
          Download PDF
        </button>
      </div>

      <div className="border border-gray-400 rounded overflow-hidden mb-10">
        <div className="bg-gray-100 p-2 font-bold border-b border-gray-400">
          Abstract
        </div>
        <div className="p-4 text-justify leading-relaxed">
          {paperInfo.abstract}
        </div>
      </div>

      <div className="flex justify-center">
        <button className="bg-[#FF5F5F] text-white px-10 py-2 rounded-xl font-bold shadow-md hover:bg-red-500 transition-colors">
          Review
        </button>
      </div>
    </div>
  );
};

export default PaperDetail;
