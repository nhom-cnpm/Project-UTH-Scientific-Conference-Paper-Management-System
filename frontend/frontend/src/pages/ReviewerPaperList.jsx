import React from 'react';

const ReviewerPaperList = () => {
  // Dữ liệu mẫu (bạn có thể thay bằng gọi API sau)
  const papers = [
    { id: 1, title: "Nghiên cứu về AI trong y tế", status: "Pending" },
    { id: 2, title: "Ứng dụng Blockchain trong giáo dục", status: "Reviewed" },
  ];

  return (
    <div>
      <h3>Danh sách bài báo cần đánh giá</h3>
      <table border="1" cellPadding="10" style={{ width: '100%', marginTop: '10px', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#eee' }}>
            <th>ID</th>
            <th>Tên bài báo</th>
            <th>Trạng thái</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {papers.map(paper => (
            <tr key={paper.id}>
              <td>{paper.id}</td>
              <td>{paper.title}</td>
              <td>{paper.status}</td>
              <td>
                <button>Xem chi tiết</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ReviewerPaperList;