function SprintList({
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
}) {
    return (
        <>
            <div className="issue-header">
                <div>
                    <h1>Sprints</h1>
                </div>

                <button
                    className="new-project-btn"
                    onClick={() => setShowCreateModal(true)}
                >
                    + Create Sprint
                </button>
            </div>

            <div className="issue-toolbar">
                <div>
                    <label>Project</label>
                    <select
                        value={selectedProjectId}
                        onChange={(e) => {
                            setSelectedProjectId(e.target.value);
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

                <form className="sprint-search-box">
                    <label>Search</label>
                    <input
                        placeholder="Search sprint..."
                        value={search}
                        onChange={(e) => {
                            setSearch(e.target.value);
                            setPage(1);
                        }}
                    />
                </form>
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
                                onClick={() => setShowCreateModal(false)}
                            >
                                ×
                            </button>
                        </div>

                        <form onSubmit={handleCreateSprint}>
                            <label>Project</label>
                            <select
                                value={sprintData.project_id}
                                onChange={(e) =>
                                    setSprintData({
                                        ...sprintData,
                                        project_id: e.target.value,
                                    })
                                }
                            >
                                {projects.map((project) => (
                                    <option key={project.project_id} value={project.project_id}>
                                        {project.name}
                                    </option>
                                ))}
                            </select>

                            <label>Sprint Name</label>
                            <input
                                value={sprintData.name}
                                onChange={(e) =>
                                    setSprintData({ ...sprintData, name: e.target.value })
                                }
                                placeholder="Sprint 1"
                            />

                            <label>Start Date</label>
                            <input
                                type="date"
                                value={sprintData.start_date}
                                onChange={(e) =>
                                    setSprintData({
                                        ...sprintData,
                                        start_date: e.target.value,
                                    })
                                }
                            />

                            <label>End Date</label>
                            <input
                                type="date"
                                value={sprintData.end_date}
                                onChange={(e) =>
                                    setSprintData({
                                        ...sprintData,
                                        end_date: e.target.value,
                                    })
                                }
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
        </>
    );
}

export default SprintList;
