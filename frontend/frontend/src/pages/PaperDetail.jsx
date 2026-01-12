import ReviewForm from "../../components/ReviewForm";

export default function PaperDetail() {
  return (
    <div>
      <h2>Paper Detail</h2>

      <div
        style={{
          height: 300,
          border: "1px solid gray",
          marginBottom: 20,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        PDF Viewer (mock)
      </div>

      <ReviewForm />
    </div>
  );
}
