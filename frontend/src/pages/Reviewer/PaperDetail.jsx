import { useParams } from "react-router-dom";
import { papers } from "../../data/mockPapers";
import ReviewForm from "../../components/ReviewForm";

export default function PaperDetail() {
  const { id } = useParams();
  const paper = papers.find((p) => p.id === Number(id));

  if (!paper) return <p>Paper not found</p>;

  return (
    <div>
      <h3>{paper.title}</h3>

      <iframe src={paper.pdf} width="100%" height="500px" title="PDF Viewer" />

      <ReviewForm />
    </div>
  );
}
