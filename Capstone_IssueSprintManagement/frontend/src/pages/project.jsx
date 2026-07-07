import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import ProjectList from "../components/projects/ProjectList";
import ProjectDetail from "../components/projects/ProjectDetail";

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
          <ProjectList
            user={user}
            isAdmin={isAdmin}
            projects={projects}
            setSelectedProject={setSelectedProject}
            setShowCreateModal={setShowCreateModal}
            showCreateModal={showCreateModal}
            projectData={projectData}
            handleCreateChange={handleCreateChange}
            handleCreateProject={handleCreateProject}
            setShowDeleteModal={setShowDeleteModal}
            setProjectToDelete={setProjectToDelete}
            showDeleteModal={showDeleteModal}
            projectToDelete={projectToDelete}
            handleDeleteProject={handleDeleteProject}
            setProjectToDelete={setProjectToDelete}
          />
        ) : (
          <ProjectDetail
            isAdmin={isAdmin}
            selectedProject={selectedProject}
            setSelectedProject={setSelectedProject}
            openEditModal={openEditModal}
            showEditModal={showEditModal}
            setShowEditModal={setShowEditModal}
            editData={editData}
            handleEditChange={handleEditChange}
            handleUpdateProject={handleUpdateProject}
            availableMembers={availableMembers}
            selectedMemberId={selectedMemberId}
            setSelectedMemberId={setSelectedMemberId}
            handleAddMember={handleAddMember}
            handleRemoveMember={handleRemoveMember}
          />
        )}
      </main>
    </div>
  );
}

export default Project;
