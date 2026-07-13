import { useEffect, useState } from "react";
import { FiArrowLeft, FiEdit2 } from "react-icons/fi";
import Sidebar from "../components/Sidebar";
import {
  getProjects,
  createProject,
  updateProject,
  deleteProject,
  getUsersByRole,
  addMemberToProject,
  removeMemberFromProject,
} from "../services/auth-service";
import { toast } from "react-toastify";

function Project() {
  const user = JSON.parse(localStorage.getItem("user"));
  const isAdmin = user?.role === "admin";

  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [availableMembers, setAvailableMembers] = useState([]);
  const [selectedMemberId, setSelectedMemberId] = useState("");

  const [memberAdded, setMemberAdded] = useState(false);
  const [memberRemoved, setMemberRemoved] = useState(false);
  const [descriptionUpdated, setDescriptionUpdated] = useState(false);

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);

  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [projectToDelete, setProjectToDelete] = useState(null);

  const [projectData, setProjectData] = useState({
    name: "",
    description: "",
    project_key: "",
    members: [],
  });

  const [editData, setEditData] = useState({
    name: "",
    description: "",
    project_key: "",
  });

  useEffect(() => {
    loadProjects();
    loadMembers();
  }, []);

  const getFilteredProjects = (data) => {
    if (user?.role === "admin") return data;

    return data.filter((project) =>
      project.members.some((member) => member.user_id === user.user_id),
    );
  };

  const loadProjects = async () => {
    try {
      const data = await getProjects();
      console.log("Projects from API:", data);

      setProjects(getFilteredProjects(data));
    } catch (error) {
      console.log("Project load error:", error);
      toast.error(error.detail || "Failed to load projects.");
    }
  };

  const loadMembers = async () => {
    try {
      const members = await getUsersByRole("member");
      const viewers = await getUsersByRole("viewer");
      setAvailableMembers([...members, ...viewers]);
    } catch (error) {
      toast.error(error.detail || "Failed to load users.");
    }
  };

  const refreshSelectedProject = async (projectId) => {
    const data = await getProjects();
    const filtered = getFilteredProjects(data);
    setProjects(filtered);

    const updatedProject = filtered.find(
      (project) => project.project_id === projectId,
    );

    if (updatedProject) {
      setSelectedProject(updatedProject);
    }
  };

  const handleCreateChange = (e) => {
    const { name, value } = e.target;
    setProjectData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();

    try {
      await createProject(user.user_id, projectData);

      toast.success("Project created successfully!");
      setShowCreateModal(false);

      setProjectData({
        name: "",
        description: "",
        project_key: "",
        members: [],
      });

      await loadProjects();
    } catch (error) {
      toast.error(error.detail || "Project creation failed.");
    }
  };

  const openEditModal = () => {
    setEditData({
      name: selectedProject.name,
      description: selectedProject.description,
      project_key: selectedProject.project_key,
    });

    setMemberAdded(false);
    setMemberRemoved(false);
    setDescriptionUpdated(false);
    setSelectedMemberId("");

    setShowEditModal(true);
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    if (e.target.name === "description") {
      setDescriptionUpdated(true);
    }

    setEditData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleUpdateProject = async (e) => {
    e.preventDefault();

    try {
      await updateProject(selectedProject.project_id, editData);
      await refreshSelectedProject(selectedProject.project_id);

      setShowEditModal(false);

      if (descriptionUpdated || memberAdded || memberRemoved) {
        toast.success("Project updated successfully.");
      } else {
        toast.success("No changes made.");
      }

      setMemberAdded(false);
      setMemberRemoved(false);
      setDescriptionUpdated(false);
    } catch (error) {
      toast.error(error.detail || "Project update failed.");
    }
  };

  const handleDeleteProject = async () => {
    if (!projectToDelete) return;

    try {
      const response = await deleteProject(projectToDelete.project_id);
      toast.success(response.message || "Project deleted successfully.");

      setShowDeleteModal(false);
      setProjectToDelete(null);

      await loadProjects();
    } catch (error) {
      toast.error(error.detail || "Project deletion failed.");
    }
  };

  const handleAddMember = async (memberId) => {
    if (!memberId) return;

    try {
      await addMemberToProject(selectedProject.project_id, {
        admin_id: user.user_id,
        member_id: memberId,
      });

      setMemberAdded(true);
      setSelectedMemberId("");

      await refreshSelectedProject(selectedProject.project_id);
    } catch (error) {
      toast.error(error.detail || "Add member failed.");
    }
  };

  const handleRemoveMember = async (memberId) => {
    try {
      await removeMemberFromProject(selectedProject.project_id, {
        admin_id: user.user_id,
        member_id: memberId,
      });

      setMemberRemoved(true);

      await refreshSelectedProject(selectedProject.project_id);
    } catch (error) {
      toast.error(error.detail || "Remove member failed.");
    }
  };

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <main className="dashboard-main">
        {!selectedProject ? (
          <>
            <div className="dashboard-user-row">
              <div className="dashboard-profile">
                <div className="profile-avatar">
                  {user?.name?.charAt(0).toUpperCase()}
                </div>
                <span>{user?.name}</span>
              </div>
            </div>

            <div className="dashboard-header">
              <div>
                <h1>Projects</h1>
                <p>Welcome back, {user?.name}!</p>
              </div>

              {isAdmin && (
                <button
                  className="new-project-btn"
                  onClick={() => setShowCreateModal(true)}
                >
                  {" "}
                  + New Project
                </button>
              )}
            </div>

            <div className="dashboard-stats">
              <div className="stat-card">
                <p>Total Projects</p>
                <h2>{projects.length}</h2>
              </div>

              <div className="stat-card">
                <p>Total Issues</p>
                <h2>0</h2>
              </div>

              <div className="stat-card">
                <p>Open Issues</p>
                <h2>0</h2>
              </div>

              <div className="stat-card">
                <p>Active Sprints</p>
                <h2>0</h2>
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
                      <span>{project.members.length} Members</span>
                      <span>0 Issues</span>
                    </div>

                    <div className="progress-line">
                      <div className="progress-fill" style={{ width: "0%" }} />
                    </div>

                    <p className="progress-text">0%</p>
                  </div>
                ))
              )}
            </div>
          </>
        ) : (
          <>
            <div
              className="back-link"
              onClick={() => {
                setSelectedProject(null);
                toast.dismiss();
              }}
            >
              <FiArrowLeft size={15} />
              <span>Back</span>
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
                  <FiEdit2 /> Edit Project
                </button>
              )}
            </div>

            <div className="project-tabs">
              <span className="active-tab">Overview</span>
              <span>Issues</span>
              <span>Sprints</span>
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
                <h3>Members ({selectedProject.members.length})</h3>

                <div className="members-scroll">
                  {selectedProject.members.length > 0 ? (
                    [...selectedProject.members].reverse().map((member) => (
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
                  <strong>0</strong>
                </div>

                <div className="summary-row">
                  <span>Open Issues</span>
                  <strong>0</strong>
                </div>

                <div className="summary-row">
                  <span>Closed Issues</span>
                  <strong>0</strong>
                </div>

                <div className="summary-row">
                  <span>Total Sprints</span>
                  <strong>0</strong>
                </div>
              </div>
            </div>
          </>
        )}
      </main>

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
                cols="30"
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

      {showEditModal && (
        <div className="modal-overlay">
          <div className="project-modal wide-modal">
            <div className="modal-header">
              <h2>Edit Project</h2>

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
                        <div className="modal-member-row" key={member.user_id}>
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
    </div>
  );
}

export default Project;
