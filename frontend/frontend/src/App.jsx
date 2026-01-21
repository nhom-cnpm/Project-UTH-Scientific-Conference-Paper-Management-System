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
import Home from "./pages/Home";

function App() {
  return (
    <Router>
      <Routes>
        {/* 1. Trang chủ hiện ngay lập tức tại đường dẫn gốc */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />

        {/* 2. Trang đăng nhập */}
        <Route path="/login" element={<Login />} />

        {/* 3. Chuyển Dashboard sang một đường dẫn riêng (ví dụ: /dashboard) */}
        <Route path="/dashboard" element={<DashboardLayout />}>
           {/* Các route con của dashboard đặt ở đây */}
        </Route>

        {/* 4. Route dành cho Reviewer */}
        <Route path="/reviewer" element={<ReviewerLayout />}>
          <Route index element={<Navigate to="papers" />} />
          <Route path="papers" element={<ReviewerPaperList />} />
          <Route path="paper/:id" element={<PaperDetail />} />
        </Route>

        {/* 5. Route dành cho Chair */}
        <Route path="/chair" element={<ChairLayout />}>
          {/* Thêm các trang của Chair vào đây */}
        </Route>

        {/* Redirect nếu nhập sai đường dẫn: quay về trang chủ Home */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
