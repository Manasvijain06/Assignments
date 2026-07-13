function SprintList({
    user,
    projects,
    sprints,
    selectedProjectId,
    setSelectedProjectId,
    statusFilter,
    setStatusFilter,
    search,
    setSearch,
    page,
    setPage,
    totalPages,
    setSelectedSprint,
    loadAvailableIssues,
    showCreateModal,
    setShowCreateModal,
    sprintData,
    setSprintData,
    handleCreateSprint,
    errors,
    setErrors,
}) {
    const handleSprintDataChange = (fieldName, value) => {
      setSprintData((prev) => ({
        ...prev,
        [fieldName]: value,
      }));

    setErrors((prev) => ({
    ...prev,
    [fieldName]: "",
  }));
};

    const openCreateModal = () => {
  setSprintData({
    name: "",
    project_id:
      selectedProjectId !== "all"
        ? selectedProjectId
        : projects[0]?.project_id || "",
    start_date: "",
    end_date: "",
  });

  setErrors({
    name: "",
    project_id: "",
    start_date: "",
    end_date: "",
  });

  setShowCreateModal(true);
};

const closeCreateModal = () => {
  setShowCreateModal(false);

  setSprintData({
    name: "",
    project_id:
      selectedProjectId !== "all"
        ? selectedProjectId
        : projects[0]?.project_id || "",
    start_date: "",
    end_date: "",
  });

  setErrors({
    name: "",
    project_id: "",
    start_date: "",
    end_date: "",
  });
};

    return (
      <>
        <div className="issue-header">
          <div>
            <h1>Sprints</h1>
          </div>
          {user?.role === "admin" && (
            <button
              type="button"
              className="new-project-btn"
              onClick={openCreateModal}
            >
              + Create Sprint
            </button>
          )}
        </div>

        <div className="issue-toolbar">
          <div>
            <label>Project</label>
            <select
              value={selectedProjectId}
              onChange={(e) => {
                const projectId = e.target.value;

                setSelectedProjectId(projectId);
                localStorage.setItem("selectedProjectId", projectId);
                setPage(1);
              }}
            >
              <option value="all">All Projects</option>
              {projects.map((project) => (
                <option key={project.project_id} value={project.project_id}>
                  {project.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label>Status</label>
            <select
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                setPage(1);
              }}
            >
              <option value="all">All</option>
              <option value="planned">Planned</option>
              <option value="active">Active</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          <div className="sprint-search-box">
            <label>Search</label>
            <input
              placeholder="Search sprint..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
            />
          </div>
        </div>

        <div className="issue-table-card">
          <table className="issue-table">
            <thead>
              <tr>
                <th>Sprint</th>
                <th>Status</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Progress</th>
                <th>Issues</th>
              </tr>
            </thead>

            <tbody>
              {sprints.length === 0 ? (
                <tr>
                  <td colSpan="6" className="empty-row">
                    No sprints found.
                  </td>
                </tr>
              ) : (
                sprints.map((sprint) => (
                  <tr
                    key={sprint.sprint_id}
                    className="clickable-row"
                    onClick={() => {
                      setSelectedSprint(sprint);
                      loadAvailableIssues(sprint.project_id);
                    }}
                  >
                    <td>{sprint.name}</td>
                    <td>
                      <span className={`sprint-status ${sprint.status}`}>
                        {sprint.status}
                      </span>
                    </td>
                    <td>{sprint.start_date}</td>
                    <td>{sprint.end_date}</td>
                    <td>
                      <div className="sprint-progress-cell">
                        <div className="sprint-progress-bar">
                          <div
                            className="sprint-progress-fill"
                            style={{ width: `${sprint.progress}%` }}
                          />
                        </div>
                        <span>{sprint.progress}%</span>
                      </div>
                    </td>
                    <td>
                      {sprint.completed_issues}/{sprint.total_issues}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
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
                <h2>Create Sprint</h2>

                <button
                  type="button"
                  className="modal-close"
                  onClick={closeCreateModal}
                >
                  ×
                </button>
              </div>

              <form onSubmit={handleCreateSprint}>
                <label>Project</label>
                <select
                  value={sprintData.project_id}
                  onChange={(e) =>
                    handleSprintDataChange("project_id", e.target.value)
                  }
                >
                  <option value="">Select Project</option>
                  {projects.map((project) => (
                    <option key={project.project_id} value={project.project_id}>
                      {project.name}
                    </option>
                  ))}
                </select>
                {errors.project_id && (
                  <p className="error">{errors.project_id}</p>
                )}

                <label>Sprint Name</label>
                <input
                  value={sprintData.name}
                  onChange={(e) =>
                    handleSprintDataChange("name", e.target.value)
                  }
                  placeholder="Sprint 1"
                />

                {errors.name && <p className="error">{errors.name}</p>}

                <label>Start Date</label>
                <input
                  type="date"
                  value={sprintData.start_date}
                  onChange={(e) =>
                    handleSprintDataChange("start_date", e.target.value)
                  }
                />

                {errors.start_date && (
                  <p className="error">{errors.start_date}</p>
                )}

                <label>End Date</label>
                <input
                  type="date"
                  value={sprintData.end_date}
                  onChange={(e) =>
                    handleSprintDataChange("end_date", e.target.value)
                  }
                />
                {errors.end_date && <p className="error">{errors.end_date}</p>}

                <div className="modal-actions">
                  <button type="submit" className="modal-create-btn">
                    Create
                  </button>

                  <button
                    type="button"
                    className="modal-cancel-btn"
                    onClick={closeCreateModal}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </>
    );
}

export default SprintList;
