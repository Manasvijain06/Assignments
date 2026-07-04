import { NavLink, useNavigate } from "react-router-dom";
import {
  FiHome,
  FiFolder,
  FiFlag,
  FiClipboard,
  FiUser,
  FiLogOut,
} from "react-icons/fi";

function Sidebar() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));

  const handleLogout = () => {
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <aside className="dashboard-sidebar">
      <div className="sidebar-logo">
        <div>
          <h2>
            Issue & Sprint <br /> Management
          </h2>
        </div>
      </div>

      <nav className="sidebar-menu">
        <NavLink to="/projects" className="sidebar-item">
          <FiFolder />
          <span>Projects</span>
        </NavLink>

        <NavLink to="/issues" className="sidebar-item">
          <FiFlag />
          <span>Issues</span>
        </NavLink>

        <NavLink to="/sprints" className="sidebar-item">
          <FiClipboard />
          <span>Sprints</span>
        </NavLink>

        <NavLink to="/profile" className="sidebar-item">
          <FiUser />
          <span>Profile</span>
        </NavLink>
      </nav>

      <button className="sidebar-logout" onClick={handleLogout}>
        <FiLogOut />
        <span>Logout</span>
      </button>
    </aside>
  );
}

export default Sidebar;
