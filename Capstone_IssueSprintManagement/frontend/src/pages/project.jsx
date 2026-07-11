import { useEffect, useState } from "react";
import {
  getProjects,
  updateProject,
  getUsersByRole,
  addMemberToProject,
  removeMemberFromProject,
} from "../services/auth-service";

function Project() {
  const [projects, setProjects] = useState([]);
  const [members, setMembers] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [message, setMessage] = useState("");

  const [editData, setEditData] = useState({
    name: "",
    description: "",
    project_key: "",
  });

  const [memberEmail, setMemberEmail] = useState("");

  useEffect(() => {
    loadProjects();
    loadMembers();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await getProjects();

      setProjects(data);

      if (data.length > 0) {
        setSelectedProject(data[0]);
      }
    } catch (error) {
      setMessage(error.detail || "Failed to load projects.");
    }
  };

  const loadMembers = async () => {
    try {
      const data = await getUsersByRole("member");
      setMembers(data);
    } catch (error) {
      setMessage(error.detail || "Failed to load members.");
    }
  };

  const selectProject = (project) => {
    setSelectedProject(project);
    setEditData({
      name: project.name,
      description: project.description,
      project_key: project.project_key,
    });
    setMemberEmail("");
    setMessage("");
  };

  const handleUpdateProject = async () => {
    try {
      const response = await updateProject(
        selectedProject.project_id,
        editData,
      );

      setMessage(response.message);
      await loadProjects();
    } catch (error) {
      setMessage(error.detail || "Project update failed.");
    }
  };

  const handleAddMember = async () => {
    try {
      const adminEmail = selectedProject.created_by;

      const response = await addMemberToProject(selectedProject.project_id, {
        admin_email: adminEmail,
        member_email: memberEmail,
      });

      setMessage(response.message);
      await loadProjects();
    } catch (error) {
      setMessage(error.detail || "Add member failed.");
    }
  };

  const handleRemoveMember = async (email) => {
    try {
      const adminEmail = selectedProject.created_by;

      const response = await removeMemberFromProject(
        selectedProject.project_id,
        {
          admin_email: adminEmail,
          member_email: email,
        },
      );

      setMessage(response.message);
      await loadProjects();
    } catch (error) {
      setMessage(error.detail || "Remove member failed.");
    }
  };

  return (
    <div className="container">
      <h2>Projects</h2>

      <div className="project-content">
        <div className="project-card">
          <h3>Project List</h3>

          {projects.length === 0 ? (
            <p>No projects found.</p>
          ) : (
            projects.map((project) => (
              <div
                key={project.project_id}
                className="project-list-item"
                onClick={() => selectProject(project)}
              >
                <strong>{project.name}</strong>
                <p>{project.project_key}</p>
              </div>
            ))
          )}
        </div>

        {selectedProject && (
          <div className="project-card">
            <h3>Project Details</h3>

            <p>
              <strong>Description:</strong> {selectedProject.description}
            </p>

            <p>
              <strong>Project Lead:</strong> {selectedProject.created_by}
            </p>

            <hr />

            <h3>Edit Project</h3>

            <input
              type="text"
              value={editData.name}
              placeholder="Project name"
              onChange={(e) =>
                setEditData({ ...editData, name: e.target.value })
              }
            />

            <input
              type="text"
              value={editData.description}
              placeholder="Description"
              onChange={(e) =>
                setEditData({ ...editData, description: e.target.value })
              }
            />

            <input
              type="text"
              value={editData.project_key}
              placeholder="Project key"
              onChange={(e) =>
                setEditData({ ...editData, project_key: e.target.value })
              }
            />

            <button onClick={handleUpdateProject}>Update Project</button>

            <hr />

            <h3>Manage Members</h3>

            <select
              value={memberEmail}
              onChange={(e) => setMemberEmail(e.target.value)}
            >
              <option value="">Select Member</option>
              {members.map((member) => (
                <option key={member.email} value={member.email}>
                  {member.name} ({member.email})
                </option>
              ))}
            </select>

            <button onClick={handleAddMember}>Add Member</button>

            <h4>Assigned Members</h4>

            {selectedProject.members?.length > 0 ? (
              selectedProject.members.map((email) => (
                <div key={email}>
                  {email}
                  <button onClick={() => handleRemoveMember(email)}>
                    Remove
                  </button>
                </div>
              ))
            ) : (
              <p>No members assigned.</p>
            )}
          </div>
        )}
      </div>

      {message && (
        <p className={message.includes("successfully") ? "success" : "error"}>
          {message}
        </p>
      )}
    </div>
  );
}

export default Project;
