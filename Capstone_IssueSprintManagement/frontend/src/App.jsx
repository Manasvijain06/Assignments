import { Routes, Route, Navigate } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/login";
import ProjectManagement from "./pages/Project";
import Issue from "./pages/issue";
import Sprint from "./pages/Sprint";
import Profile from "./pages/Profile";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />

      <Route path="/register" element={<Register />} />

      <Route path="/login" element={<Login />} />

      <Route path="/projects" element={<ProjectManagement />} />

      <Route path="/issues" element={<Issue />} />

      <Route path="/sprints" element={<Sprint />} />

      <Route path="/profile" element={<Profile />} />
    </Routes>
  );
}

export default App;
