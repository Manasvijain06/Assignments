function ProjectDetail({
  isAdmin,
  dashboardStats,
  selectedProject,
  setSelectedProject,
  openEditModal,
  showEditModal,
  setShowEditModal,
  editData,
  handleEditChange,
  handleUpdateProject,
  availableMembers,
  selectedMemberId,
  setSelectedMemberId,
  handleAddMember,
  handleRemoveMember,
}) {
    const members = selectedProject.members || [];
    return (
      <>
        <div
          className="back-link"
          onClick={() => {
            setSelectedProject(null);
          }}
        >
          <span>← Back</span>
        </div>

        <div className="project-detail-header">
          <div className="project-title-box">
            <div className="project-logo">
              {selectedProject.project_key.slice(0, 2).toUpperCase()}
            </div>

            <div>
              <h1>{selectedProject.name}</h1>
              <p>{selectedProject.description}</p>
            </div>
          </div>

          {isAdmin && (
            <button className="edit-project-btn" onClick={openEditModal}>
              ✎ Edit Project
            </button>
          )}
        </div>

        <div className="project-tabs">
          <span className="active-tab">Overview</span>
        </div>

        <div className="project-overview-grid">
          <div className="overview-card">
            <h3>Project Details</h3>

            <p className="label">Project Key</p>
            <p>{selectedProject.project_key}</p>

            <p className="label">Project Lead</p>
            <p>{selectedProject.created_by?.name || "N/A"}</p>

            <p className="label">Description</p>
            <p>{selectedProject.description}</p>
          </div>

          <div className="overview-card">
            <h3>Members ({members.length})</h3>

            <div className="members-scroll">
              {members.length > 0 ? (
                [...members].reverse().map((member) => (
                  <div className="member-preview" key={member.user_id}>
                    <div className="member-avatar">
                      {member.name.charAt(0).toUpperCase()}
                    </div>

                    <div className="member-info">
                      <strong>{member.name}</strong>
                      <p>{member.role}</p>
                    </div>
                  </div>
                ))
              ) : (
                <p>No members assigned.</p>
              )}
            </div>
          </div>

          <div className="overview-card">
            <h3>Summary</h3>

            <div className="summary-row">
              <span>Total Issues</span>
              <strong>{dashboardStats.totalIssues}</strong>
            </div>

            <div className="summary-row">
              <span>Open Issues</span>
              <strong>{dashboardStats.openIssues}</strong>
            </div>

            <div className="summary-row">
              <span>Active Sprints</span>
              <strong>{dashboardStats.activeSprints}</strong>
            </div>
          </div>
        </div>

        {showEditModal && (
          <div className="modal-overlay">
            <div className="project-modal wide-modal">
              <div className="modal-header">
                <h2> Edit Project</h2>

                <button
                  type="button"
                  className="modal-close"
                  onClick={() => setShowEditModal(false)}
                >
                  ×
                </button>
              </div>

              <form onSubmit={handleUpdateProject}>
                <div className="edit-modal-grid">
                  <div className="edit-section">
                    <h3>Project Information</h3>

                    <label>Project Name</label>
                    <input
                      type="text"
                      value={editData.name}
                      disabled
                      className="readonly-input"
                    />

                    <label>Description</label>
                    <textarea
                      name="description"
                      value={editData.description}
                      onChange={handleEditChange}
                      placeholder="Enter project description"
                    />

                    <label>Project Key</label>
                    <input
                      type="text"
                      value={editData.project_key}
                      disabled
                      className="readonly-input"
                    />
                  </div>

                  <div className="edit-section">
                    <h3>Manage Members</h3>

                    <label>Add Member</label>
                    <select
                      value={selectedMemberId}
                      onChange={(e) => {
                        setSelectedMemberId(e.target.value);
                        handleAddMember(e.target.value);
                      }}
                    >
                      <option value="">Select member to add</option>

                      {availableMembers.map((member) => (
                        <option key={member.user_id} value={member.user_id}>
                          {member.name} ({member.role}) - {member.email}
                        </option>
                      ))}
                    </select>

                    <label>Assigned Members</label>

                    <div className="assigned-member-list">
                      {selectedProject.members.length > 0 ? (
                        selectedProject.members.map((member) => (
                          <div
                            className="modal-member-row"
                            key={member.user_id}
                          >
                            <span>{member.name}</span>

                            <button
                              type="button"
                              onClick={() => handleRemoveMember(member.user_id)}
                            >
                              ×
                            </button>
                          </div>
                        ))
                      ) : (
                        <p>No members assigned.</p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="modal-actions">
                  <button type="submit" className="modal-create-btn">
                    Update
                  </button>

                  <button
                    type="button"
                    className="modal-cancel-btn"
                    onClick={() => setShowEditModal(false)}
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

export default ProjectDetail;
