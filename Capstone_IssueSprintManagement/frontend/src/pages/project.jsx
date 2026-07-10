import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import ProjectList from "../components/projects/ProjectList";
import ProjectDetail from "../components/projects/ProjectDetail";
import Notification from "../components/Notification";
import {
  getProjects,
  addMemberToProject,
  createProject,
  updateProject,
  deleteProject,
  getUsersByRole,
  removeMemberFromProject,
  getProjectIssues,
  getSprints,
} from "../services/auth-service";

const initialProjectData = {
  name: "",
  description: "",
  project_key: "",
  members: [],
};

const initialEditData = {
  name: "",
  description: "",
  project_key: "",
};

const initialDashboardStats = {
  totalIssues: 0,
  openIssues: 0,
  closedIssues: 0,
  activeSprints: 0,
};

function Project() {

  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const isAdmin = user?.role === "admin";

  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [availableMembers, setAvailableMembers] = useState([]);
  const [selectedMemberId, setSelectedMemberId] = useState("");

  const [dashboardStats, setDashboardStats] = useState(initialDashboardStats);

  const [memberAdded, setMemberAdded] = useState(false);
  const [memberRemoved, setMemberRemoved] = useState(false);
  const [descriptionUpdated, setDescriptionUpdated] = useState(false);

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);

  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [projectToDelete, setProjectToDelete] = useState(null);

  const [projectData, setProjectData] = useState(initialProjectData);
  const [editData, setEditData] = useState(initialEditData);

  const [notification, setNotification] = useState({
    message: "",
    type: "",
  });

  useEffect(() => {
    loadProjects();
    loadMembers();
  }, []);

  const showNotification = (message, type = "success") => {
    setNotification({ message, type });

    setTimeout(() => {
      setNotification({ message: "", type: "" });
    }, 3000);
  };

  const getFilteredProjects = (projectList) => {
    if (isAdmin) {
      return projectList;
    }

    return projectList.filter((project) =>
      (project.members || []).some((member) => member.user_id === user.user_id),
    );
  };

  const loadProjects = async () => {
    try {
      const data = await getProjects();
      const filteredProjects = getFilteredProjects(data);

      setProjects(getFilteredProjects(data));
      await loadDashboardStats(filteredProjects);
    } catch (error) {
      showNotification(error.detail || "Failed to load projects.","error");
    }
  };

  const loadMembers = async () => {
    try {
      const members = await getUsersByRole("member");
      const viewers = await getUsersByRole("viewer");

      setAvailableMembers([...members, ...viewers]);
    } catch (error) {
      showNotification(error.detail || "Failed to load users.","error");
    }
  };

  const refreshSelectedProject = async (projectId) => {
    const data = await getProjects();
    const filteredProjects = getFilteredProjects(data);

    setProjects(filteredProjects);

    const updatedProject = filteredProjects.find(
      (project) => project.project_id === projectId,
    );

    if (updatedProject) {
      setSelectedProject(updatedProject);
    }
  };

  const resetEditFlags = () => {
    setMemberAdded(false);
    setMemberRemoved(false);
    setDescriptionUpdated(false);
  };

  const handleCreateChange = (event) => {
    const { name, value } = event.target;

    setProjectData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();

    try {
      await createProject(user.user_id, projectData);

      showNotification("Project created successfully!","success");
      setShowCreateModal(false);
      setProjectData(initialProjectData);

      await loadProjects();
    } catch (error) {
      showNotification(error.detail || "Project creation failed.","error");
    }
  };

  const openEditModal = () => {
    setEditData({
      name: selectedProject.name,
      description: selectedProject.description,
      project_key: selectedProject.project_key,
    });

    resetEditFlags();
    setSelectedMemberId("");
    setShowEditModal(true);
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;

    if (name === "description") {
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
        showNotification("Project updated successfully.", "success");
      } else {
        showNotification("No changes made.","success");
      }

      resetEditFlags();
    } catch (error) {
      showNotification(error.detail || "Project update failed.","error");
    }
  };

  const handleDeleteProject = async () => {
    if (!projectToDelete) return;

    try {
      await deleteProject(projectToDelete.project_id);

      showNotification("Project deleted successfully.","success");

      setShowDeleteModal(false);
      setProjectToDelete(null);

      await loadProjects();
    } catch (error) {
      showNotification(error.detail || "Project deletion failed.","error");
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
      showNotification(error.detail || "Add member failed.","error");
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
      showNotification(error.detail || "Remove member failed.","error");
    }
  };

  const loadDashboardStats = async (projectList) => {
    try {
      let totalIssues = 0;
      let openIssues = 0;
      let closedIssues = 0;
      let activeSprints = 0;

      for (const project of projectList) {
        const issueResponse = await getProjectIssues(project.project_id, {
          page: 1,
          limit: 50,
          status: "all",
          priority: "all",
          assignee: "all",
          search: "",
        });

        const allIssues = issueResponse.items.flatMap((issue) => [
          issue,
          ...(issue.children || []),
        ]);

        totalIssues += allIssues.length;
        closedIssues += allIssues.filter(
          (issue) => issue.status === "done",
        ).length;
        openIssues += allIssues.filter(
          (issue) => issue.status !== "done",
        ).length;
      }

      const sprintResponse = await getSprints({
        page: 1,
        limit: 50,
        project_id: "all",
        status: "active",
        search: "",
      });

      activeSprints = sprintResponse.items.length;

      setDashboardStats({
        totalIssues,
        openIssues,
        closedIssues,
        activeSprints,
      });
    } catch (error) {
      showNotification(error.detail || "Failed to load dashboard stats.","error");
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
            dashboardStats={dashboardStats}
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
          />
        ) : (
          <ProjectDetail
            isAdmin={isAdmin}
            dashboardStats={dashboardStats}
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
      <Notification
        message={notification.message}
        type={notification.type}
        onClose={() => setNotification({ message: "", type: "" })}
      />
    </div>
  );
}

export default Project;
