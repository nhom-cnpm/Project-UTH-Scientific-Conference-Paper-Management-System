import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import DashboardLayout from "./layouts/DashboardLayout";
import ReviewerLayout from "./layouts/ReviewerLayout";
import ChairLayout from "./layouts/ChairLayout";
import ReviewerPaperList from "./pages/ReviewerPaperList";
import PaperDetail from "./pages/PaperDetail";
import Login from "./pages/Login";

function App() {
  return (
    <Router>
      <Routes>
        {/* Route cho Login */}
        <Route path="/login" element={<Login />} />

        {/* Route dành cho Reviewer */}
        <Route path="/reviewer" element={<ReviewerLayout />}>
          <Route index element={<Navigate to="papers" />} />
          <Route path="papers" element={<ReviewerPaperList />} />
          <Route path="paper/:id" element={<PaperDetail />} />
        </Route>

        {/* Route dành cho Chair */}
        <Route path="/chair" element={<ChairLayout />}>
          {/* Thêm các trang của Chair vào đây */}
        </Route>

        {/* Route mặc định (Dashboard) */}
        <Route path="/" element={<DashboardLayout />}>
          {/* Các nội dung mặc định của Dashboard */}
        </Route>

        {/* Redirect nếu không tìm thấy trang */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
