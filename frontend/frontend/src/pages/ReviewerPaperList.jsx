import { Link } from "react-router-dom";
import { papers } from "../data/mockPapers";

export default function ReviewerPaperList() {
  return (
    <div>
      <h3>Assigned Papers</h3>
      <ul>
        {papers.map((p) => (
          <li key={p.id}>
            {p.title}
            {" | "}
            <Link to={`/paper/${p.id}`}>Review</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
