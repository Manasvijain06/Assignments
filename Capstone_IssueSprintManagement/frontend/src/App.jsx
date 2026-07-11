import { Routes, Route, Navigate } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/login";
import ProjectManagement from "./pages/Project";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/register" />} />

      <Route path="/register" element={<Register />} />

      <Route path="/login" element={<Login />} />

      <Route path="/projects" element={<ProjectManagement />} />
    </Routes>
  );
}

export default App;
