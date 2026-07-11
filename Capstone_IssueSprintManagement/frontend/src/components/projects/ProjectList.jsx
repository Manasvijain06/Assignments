function ProjectList({
  user,
  isAdmin,
  projects,
  totalProjects,
  page,
  setPage,
  totalPages,
  dashboardStats,
  setSelectedProject,
  setShowCreateModal,
  showCreateModal,
  projectData,
  handleCreateChange,
  handleCreateProject,
  setShowDeleteModal,
  setProjectToDelete,
  showDeleteModal,
  projectToDelete,
  handleDeleteProject,
}) {
  return (
    <>
      <div className="dashboard-header">
        <div>
          <h1>Projects</h1>
          <p>Welcome back, {user?.name}!</p>
        </div>

        {isAdmin && (
          <button
            type="button"
            className="new-project-btn"
            onClick={() => setShowCreateModal(true)}
          >
            + New Project
          </button>
        )}
      </div>
      <div className="dashboard-stats">
        <div className="stat-card">
          <p>Total Projects</p>
          <h2>{totalProjects}</h2>
        </div>

        <div className="stat-card">
          <p>Total Issues</p>
          <h2>{dashboardStats.totalIssues}</h2>
        </div>

        <div className="stat-card">
          <p>Open Issues</p>
          <h2>{dashboardStats.openIssues}</h2>
        </div>

        <div className="stat-card">
          <p>Active Sprints</p>
          <h2>{dashboardStats.activeSprints}</h2>
        </div>
      </div>

      <div className="project-section-header">
        <h2>{isAdmin ? "All Projects" : "My Projects"}</h2>
      </div>

      <div className="dashboard-project-grid">
        {projects.length === 0 ? (
          <p>No projects found.</p>
        ) : (
          projects.map((project) => (
            <div
              className="dashboard-project-card"
              key={project.project_id}
              onClick={() => setSelectedProject(project)}
            >
              <div className="project-card-header">
                <div className="project-avatar">
                  {project.project_key.slice(0, 2).toUpperCase()}
                </div>

                <div>
                  <h3>{project.name}</h3>
                  <p>{project.description}</p>
                </div>
              </div>

              <div className="project-card-info">
                {isAdmin && (
                  <button
                    type="button"
                    className="project-delete-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      setProjectToDelete(project);
                      setShowDeleteModal(true);
                    }}
                  >
                    Delete
                  </button>
                )}

                <span>{project.members?.length || 0} Members</span>
                <span>{project.issue_count || 0} Issues</span>
              </div>
            </div>
          ))
        )}
      </div>
      <div className="pagination">
        <button
          disabled={page === 1}
          onClick={() => setPage((prev) => prev - 1)}
        >
          ‹
        </button>

        {[...Array(totalPages)].map((_, index) => (
          <button
            key={index + 1}
            className={page === index + 1 ? "active-page" : ""}
            onClick={() => setPage(index + 1)}
          >
            {index + 1}
          </button>
        ))}

        <button
          disabled={page === totalPages}
          onClick={() => setPage((prev) => prev + 1)}
        >
          ›
        </button>
      </div>

      {showCreateModal && (
        <div className="modal-overlay">
          <div className="project-modal">
            <div className="modal-header">
              <h2>Create New Project</h2>

              <button
                type="button"
                className="modal-close"
                onClick={() => setShowCreateModal(false)}
              >
                ×
              </button>
            </div>

            <form onSubmit={handleCreateProject}>
              <label>Project Name</label>
              <input
                type="text"
                name="name"
                value={projectData.name}
                onChange={handleCreateChange}
                placeholder="Enter project name"
              />

              <label>Description</label>
              <textarea
                name="description"
                rows="3"
                value={projectData.description}
                onChange={handleCreateChange}
                placeholder="Enter project description"
              />

              <label>Project Key</label>
              <input
                type="text"
                name="project_key"
                value={projectData.project_key}
                onChange={handleCreateChange}
                placeholder="Example: ISM"
              />

              <div className="modal-actions">
                <button type="submit" className="modal-create-btn">
                  Create
                </button>

                <button
                  type="button"
                  className="modal-cancel-btn"
                  onClick={() => setShowCreateModal(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showDeleteModal && (
        <div className="modal-overlay">
          <div className="delete-modal">
            <h2>Delete Project</h2>

            <p>
              Are you sure you want to delete
              <strong> {projectToDelete?.name}</strong>?
            </p>

            <p className="delete-warning">This action cannot be undone.</p>

            <div className="modal-actions">
              <button
                type="button"
                className="delete-confirm-btn"
                onClick={handleDeleteProject}
              >
                Delete
              </button>

              <button
                type="button"
                className="modal-cancel-btn"
                onClick={() => {
                  setShowDeleteModal(false);
                  setProjectToDelete(null);
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default ProjectList;
