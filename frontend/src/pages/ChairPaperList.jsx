import { useState } from "react";
import { papers as initialPapers } from "../data/mockPapers";

export default function ChairPaperList() {
  const [papers, setPapers] = useState(initialPapers);

  const decide = (id, status) => {
    setPapers(papers.map((p) => (p.id === id ? { ...p, status } : p)));
  };

  return (
    <div>
      <h3>Paper Decisions</h3>

      {papers.map((p) => (
        <div
          key={p.id}
          style={{
            border: "1px solid #ccc",
            padding: 10,
            marginBottom: 10,
            background:
              p.status === "accepted"
                ? "#dff8e5"
                : p.status === "rejected"
                  ? "#f8d7da"
                  : "#fff",
          }}
        >
          <h4>{p.title}</h4>

          <p>
            Status: <b>{p.status}</b>
          </p>

          <h5>Reviews:</h5>
          <ul>
            {p.reviewers.map((r, i) => (
              <li key={i}>
                {r.name}: {r.score}  {r.comment}
              </li>
            ))}
          </ul>

          <button onClick={() => decide(p.id, "accepted")}>Accept</button>
          <button onClick={() => decide(p.id, "rejected")}>Reject</button>
        </div>
      ))}
    </div>
  );
}
