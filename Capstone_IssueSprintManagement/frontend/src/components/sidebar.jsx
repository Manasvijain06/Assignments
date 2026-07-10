import { Link, NavLink, useNavigate } from "react-router-dom";

function Sidebar() {
  const navigate = useNavigate();

  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const handleLogout = () => {
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <aside className="dashboard-sidebar">
      <div className="sidebar-logo">
        <div>
          <h2>
            Issue & Sprint
            <br />
            Management
          </h2>
        </div>
      </div>

      <nav className="sidebar-menu">
        <NavLink to="/projects" className="sidebar-item">
          <span>Projects</span>
        </NavLink>

        <NavLink to="/issues" className="sidebar-item">
          <span>Issues</span>
        </NavLink>

        <NavLink to="/sprints" className="sidebar-item">
          <span>Sprints</span>
        </NavLink>

        <NavLink to="/profile" className="sidebar-item">
          <span>Profile</span>
        </NavLink>
      </nav>

      <div className="sidebar-bottom">
        <Link to="/profile" className="sidebar-profile">
          <div className="sidebar-profile-avatar">
            {user?.name?.charAt(0).toUpperCase()}
          </div>

          <div>
            <strong>{user?.name}</strong>
            <p>{user?.role}</p>
          </div>
        </Link>

        <button className="sidebar-logout" onClick={handleLogout}>
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;
