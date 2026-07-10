function IssueList({
    projects,
    selectedProjectId,
    setSelectedProjectId,
    setPage,
    setIssues,
    loadStories,
    filters,
    setFilters,
    members,
    handleSearch,
    issues,
    renderIssueRow,
    page,
    totalPages,
    showCreateModal,
    setShowCreateModal,
    issueData,
    setIssueData,
    handleCreateIssue,
    stories,
}) {
    const handleFilterChange = (name, value) => {
      setFilters({
        ...filters,
        [name]: value,
      });
      setPage(1);
    };

    const handleIssueDataChange = (name, value) => {
      setIssueData({
        ...issueData,
        [name]: value,
      });
    };
    return (
      <>
        <div className="issue-header">
          <div>
            <h1>Issues</h1>
          </div>

          <button
            className="new-project-btn"
            onClick={() => setShowCreateModal(true)}
            disabled={!selectedProjectId}
          >
            + Create Issue
          </button>
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
                setIssues([]);
                loadStories(projectId);
              }}
            >
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
              value={filters.status}
              onChange={(e) => handleFilterChange("status", event.target.value)}
            >
              <option value="all">All</option>
              <option value="backlog">Backlog</option>
              <option value="todo">Todo</option>
              <option value="in_progress">In Progress</option>
              <option value="done">Done</option>
            </select>
          </div>

          <div>
            <label>Priority</label>
            <select
              value={filters.priority}
              onChange={(e) => handleFilterChange("status", event.target.value)}
            >
              <option value="all">All</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div>
            <label>Assignee</label>
            <select
              value={filters.assignee}
              onChange={(e) => handleFilterChange("status", event.target.value)}
            >
              <option value="all">All</option>
              {members.map((member) => (
                <option key={member.user_id} value={member.user_id}>
                  {member.name}
                </option>
              ))}
            </select>
          </div>

          <form onSubmit={handleSearch} className="issue-search">
            <label>Search</label>
            <input
              placeholder="Search issues..."
              value={filters.search}
              onChange={(e) =>
                setFilters({ ...filters, search: e.target.value })
              }
            />
          </form>
        </div>

        <div className="issue-table-card">
          <table className="issue-table">
            <thead>
              <tr>
                <th>Id</th>
                <th>Title</th>
                <th>Type</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Assignee</th>
              </tr>
            </thead>

            <tbody>
              {issues.length === 0 ? (
                <tr>
                  <td colSpan="6" className="empty-row">
                    No issues found.
                  </td>
                </tr>
              ) : (
                issues.map((issue) => (
                  <>
                    {renderIssueRow(issue)}

                    {issue.children?.map((child) =>
                      renderIssueRow(child, true),
                    )}
                  </>
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

          {showCreateModal && (
            <div className="modal-overlay">
              <div className="project-modal issue-modal">
                <div className="modal-header">
                  <h2>Create Issue</h2>

                  <button
                    type="button"
                    className="modal-close"
                    onClick={() => setShowCreateModal(false)}
                  >
                    ×
                  </button>
                </div>

                <form onSubmit={handleCreateIssue}>
                  <label>Title</label>
                  <input
                    value={issueData.title}
                    onChange={(e) =>
                      handleFilterChange("status", event.target.value)
                    }
                    placeholder="Enter issue title"
                  />

                  <label>Description</label>
                  <textarea
                    value={issueData.description}
                    onChange={(e) =>
                      setIssueData({
                        ...issueData,
                        description: e.target.value,
                      })
                    }
                    placeholder="Enter issue description"
                  />

                  <label>Priority</label>
                  <select
                    value={issueData.priority}
                    onChange={(e) =>
                      handleFilterChange("status", event.target.value)
                    }
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>

                  <label>Type</label>

                  <select
                    value={issueData.type}
                    onChange={(e) =>
                      setIssueData({
                        ...issueData,
                        type: e.target.value,
                        parent_id:
                          e.target.value === "story" ? "" : issueData.parent_id,
                      })
                    }
                  >
                    <option value="task">Task</option>
                    <option value="bug">Bug</option>
                    <option value="story">Story</option>
                  </select>

                  {issueData.type !== "story" && (
                    <>
                      <label>Parent Story</label>
                      <select
                        value={issueData.parent_id}
                        onChange={(e) =>
                          handleFilterChange("status", event.target.value)
                        }
                      >
                        <option value="">No parent story</option>

                        {stories.map((story) => (
                          <option key={story.issue_id} value={story.issue_id}>
                            {story.issue_key} - {story.title}
                          </option>
                        ))}
                      </select>
                    </>
                  )}

                  <label>Assignee</label>
                  <select
                    value={issueData.assignee}
                    onChange={(e) =>
                      handleFilterChange("status", event.target.value)
                    }
                  >
                    <option value="">Select assignee</option>
                    {members.map((member) => (
                      <option key={member.user_id} value={member.user_id}>
                        {member.name} ({member.role})
                      </option>
                    ))}
                  </select>

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
        </div>
      </>
    );
}

export default IssueList;

