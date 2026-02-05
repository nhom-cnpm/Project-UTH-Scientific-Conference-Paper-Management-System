import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import ReviewerLayout from "./layouts/ReviewerLayout";
import ChairLayout from "./layouts/ChairLayout";

import ReviewerPaperList from "./pages/ReviewerPaperList";
import PaperDetail from "./pages/PaperDetail";
import Login from "./pages/Login";
import Trangchu from "./pages/Trangchu";
import TrangcuaQtvien from "./pages/TrangcuaQtvien";
import AdminQuanli from "./pages/AdminQuanli";
import EditUser from "./pages/EditUser";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Trangchu />} />
        <Route path="/login" element={<Login />} />

        {/* ADMIN */}
        <Route path="/admin" element={<TrangcuaQtvien />} />
        <Route path="/adminPhanquyen" element={<TrangcuaQtvien />} />
        <Route path="/conference-manage" element={<AdminQuanli />} />
        <Route path="/conference-manage/edit" element={<EditUser />} />
    q
        {/* CHAIR */}
        <Route path="/chair" element={<ChairLayout />} />

        {/* REVIEWER */}
        <Route path="/reviewer" element={<ReviewerLayout />}>
          <Route index element={<ReviewerPaperList />} />
          <Route path="paper/:id" element={<PaperDetail />} />
        </Route>

        {/* FALLBACK */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
