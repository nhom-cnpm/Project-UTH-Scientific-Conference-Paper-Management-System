import { useState } from "react";

export default function ReviewForm() {
  const [score, setScore] = useState("");
  const [comment, setComment] = useState("");

  const submitReview = () => {
    alert(`Submitted: Score ${score}, Comment: ${comment}`);
  };

  return (
    <div>
      <h4>Review Form</h4>

      <label>Score (1-10)</label>
      <br />
      <input
        type="number"
        value={score}
        onChange={(e) => setScore(e.target.value)}
      />

      <br />
      <br />

      <label>Comment</label>
      <br />
      <textarea
        rows="4"
        value={comment}
        onChange={(e) => setComment(e.target.value)}
      />

      <br />
      <br />
      <button onClick={submitReview}>Submit Review</button>
    </div>
  );
}
