export default function ReviewForm() {
  return (
    <form>
      <h3>Submit Review</h3>

      <label>Score:</label>
      <select>
        <option>1</option>
        <option>2</option>
        <option>3</option>
        <option>4</option>
        <option>5</option>
      </select>

      <br />
      <br />

      <label>Comment:</label>
      <br />
      <textarea rows="4" cols="40" />

      <br />
      <br />
      <button type="submit">Submit</button>
    </form>
  );
}
