const mockData = [
  {
    id: 1,
    title: "Paper A",
    avgScore: 4.3,
    totalReviews: 3,
  },
  {
    id: 2,
    title: "Paper B",
    avgScore: 3.8,
    totalReviews: 2,
  },
];

export default function ChairPaperList() {
  return (
    <div>
      <h2>Submitted Papers</h2>

      {mockData.map((paper) => (
        <div key={paper.id} style={{ marginBottom: 10 }}>
          <b>{paper.title}</b>
          <p>Average Score: {paper.avgScore}</p>
          <p>Total Reviews: {paper.totalReviews}</p>
        </div>
      ))}
    </div>
  );
}
