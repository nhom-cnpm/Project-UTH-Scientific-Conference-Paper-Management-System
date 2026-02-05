const Dashboard = () => {
  const stats = [
    { label: "Assigned", count: 5, color: "bg-[#FF6B6B]" },
    { label: "Reviewed", count: 2, color: "bg-[#FF9F43]" },
    { label: "Pending", count: 3, color: "bg-[#2E5BFF]" },
  ];

  return (
    <div className="max-w-4xl mx-auto border p-6 rounded shadow-sm">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">View Assigned Papers</h2>
        <button className="text-blue-600 text-sm">View More ▾</button>
      </div>
      <div className="grid grid-cols-3 gap-6">
        {stats.map((item, index) => (
          <div
            key={index}
            className={`${item.color} text-white p-10 rounded shadow flex flex-col items-center justify-center`}
          >
            <span className="text-lg mb-2">
              {item.label === "Assigned" ? "" : item.label}
            </span>
            <span className="text-5xl font-bold">{item.count}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
