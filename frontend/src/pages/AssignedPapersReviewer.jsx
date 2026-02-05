const AssignedPapers = () => {
  const data = [
    {
      title: "Hệ thống giao thông AI",
      conf: "UTH-COMFMS",
      date: "20/03/26",
      status: "Declined",
    },
    {
      title: "Quản lý sự kiện trong trường",
      conf: "UTH-COMFMS",
      date: "",
      status: "COI",
    },
    {
      title: "Chăm sóc sức khoẻ thông minh",
      conf: "UTH-COMFMS",
      date: "22/03/26",
      status: "Reviewed",
    },
    {
      title: "Giám sát y tế cộng đồng bằng AI",
      conf: "UTH-COMFMS",
      date: "27/03/26",
      status: "Pending",
    },
    {
      title: "Hệ thống gia sư thông minh bằng AI",
      conf: "UTH-COMFMS",
      date: "22/03/26",
      status: "Pending",
    },
  ];

  return (
    <div className="w-full">
      <h2 className="text-center text-xl font-bold mb-8">
        View Assigned Papers
      </h2>
      <table className="w-full border-collapse border border-gray-200 text-sm">
        <thead>
          <tr className="bg-[#43B5AD] text-white">
            <th className="border p-3">Paper Title</th>
            <th className="border p-3">Conference</th>
            <th className="border p-3">Deadline</th>
            <th className="border p-3">Status</th>
            <th className="border p-3">Action</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, idx) => (
            <tr key={idx} className="text-center hover:bg-gray-50">
              <td className="border p-3 text-left">{item.title}</td>
              <td className="border p-3">{item.conf}</td>
              <td className="border p-3">{item.date}</td>
              <td className="border p-3">{item.status}</td>
              <td className="border p-3 text-blue-600 cursor-pointer">View</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AssignedPapers;
