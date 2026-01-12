const mockPapers = [
  { id: 1, title: "Paper A", track: "AI" },
  { id: 2, title: "Paper B", track: "SE" },
];

export default function ReviewerPaperList() {
  return (
    <div>
      <h2>Assigned Papers</h2>

      <ul>
        {mockPapers.map((paper) => (
          <li key={paper.id}>
            <b>{paper.title}</b> – Track: {paper.track}
          </li>
        ))}
      </ul>
    </div>
  );
}
