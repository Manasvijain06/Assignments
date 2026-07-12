import { useEffect, useState, } from "react";

import Sidebar from "../components/Sidebar";
import SprintList from "../components/sprints/SprintList";
import SprintDetail from "../components/sprints/SprintDetail";
import Notification from "../components/Notification";
import {
    getProjects,
    getSprints,
    createSprint,
    getProjectIssues,
    addIssueToSprint,
    startSprint,
    completeSprint,
    removeIssueFromSprint,
} from "../services/auth-service";

const initialSprintData = {
  name: "",
  project_id: "",
  start_date: "",
  end_date: "",
};

function Sprint() {
    const user = JSON.parse(localStorage.getItem("user") || "{}");

    const [projects, setProjects] = useState([]);
    const [sprints, setSprints] = useState([]);
    const [selectedProjectId, setSelectedProjectId] = useState(
      localStorage.getItem("selectedProjectId") || "all",
    );
    const [statusFilter, setStatusFilter] = useState("all");
    const [search, setSearch] = useState("");

    const [selectedSprint, setSelectedSprint] = useState(null);
    const [availableIssues, setAvailableIssues] = useState([]);
    const [selectedIssueId, setSelectedIssueId] = useState("");

    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const limit = 6;

    const [showCreateModal, setShowCreateModal] = useState(false);
    const [sprintData, setSprintData] = useState(initialSprintData);
    const [notification, setNotification] = useState({
        message: "",
        type: "",
    });

    useEffect(() => {
       loadProjects();
    }, []);

    useEffect(() => {
       loadSprints();
    }, [page, selectedProjectId, statusFilter, search]);

    const showNotification = (message, type = "success") => {
        setNotification({ message, type });

        setTimeout(() => {
            setNotification({ message: "", type: "" });
        }, 3000);
    };

    const getErrorMessage = (error, fallback) => {
      if (Array.isArray(error.detail)) {
        return error.detail[0]?.msg || fallback;
      }

      return error.detail || fallback;
    };

    const loadProjects = async () => {
      try {
        const response = await getProjects({
          page: 1,
          limit: 50,
        });

        const projectItems = response.items || [];

        const visibleProjects =
          user.role === "admin"
            ? projectItems
            : projectItems.filter((project) =>
                (project.members || []).some(
                  (member) => member.user_id === user.user_id,
                ),
              );

        setProjects(visibleProjects);

        const savedProjectId = localStorage.getItem("selectedProjectId");

        const projectExists = visibleProjects.some(
          (project) => project.project_id === savedProjectId,
        );

        if (projectExists) {
          setSelectedProjectId(savedProjectId);
        } else if (visibleProjects.length > 0) {
          const firstProjectId = visibleProjects[0].project_id;

          setSelectedProjectId(firstProjectId);
          localStorage.setItem("selectedProjectId", firstProjectId);
        } else {
          setSelectedProjectId("all");
          localStorage.removeItem("selectedProjectId");
        }
      } catch (error) {
        showNotification(
          getErrorMessage(error, "Failed to load projects."),
          "error",
        );
      }
    };

    const loadSprints = async () => {
        try {
            const response = await getSprints({
                page,
                limit,
                project_id: selectedProjectId,
                status: statusFilter,
                search,
            });

            setSprints(response.items);
            setTotalPages(response.total_pages);
        } catch (error) {
            showNotification(error.detail || "Failed to load sprints.", "error");
        }
    };

     const refreshSprints = async () => {
       const response = await getSprints({
         page,
         limit,
         project_id: selectedProjectId,
         status: statusFilter,
         search,
       });

       setSprints(response.items);
       setTotalPages(response.total_pages);

       return response.items;
     };
    
    
    const loadAvailableIssues = async (projectId) => {
        if (!projectId || projectId === "all") return;

        try {
            const response = await getProjectIssues(projectId, {
                page: 1,
                limit: 50,
                status: "all",
                priority: "all",
                assignee: "all",
                search: "",
            });

            const allIssues = response.items.flatMap((issue) => [
                issue,
                ...(issue.children || []),
            ]);

            const sprintResponse = await getSprints({
                page: 1,
                limit: 50,
                project_id: projectId,
                status: "all",
                search: "",
            });

            const assignedIssueIds = sprintResponse.items.flatMap(
                (sprint) => sprint.issues?.map((issue) => issue.issue_id) || [],
            );

            setAvailableIssues(
                allIssues.filter(
                    (issue) =>
                        issue.status !== "done" &&
                        !assignedIssueIds.includes(issue.issue_id),
                ),
            );
        } catch (error) {
            showNotification(error.detail || "Failed to load issues.", "error");
        }
    };


    const handleAddIssueToSprint = async () => {
        if (!selectedIssueId) {
            showNotification("Please select an issue.", "error");
            return;
        }

        try {
            await addIssueToSprint(selectedSprint.sprint_id, {
                issue_id: selectedIssueId,
            });

            showNotification("Issue added to sprint.", "success");
            setSelectedIssueId("");

            const updatedSprints = await refreshSprints();
            const updatedSprint = updatedSprints.find(
              (sprint) => sprint.sprint_id === selectedSprint.sprint_id,
            );

            if (updatedSprint) {
              setSelectedSprint(updatedSprint);
            }

            await loadAvailableIssues(selectedSprint.project_id);
        } catch (error) {
            showNotification(getErrorMessage(error, "Failed to add issue."), "error");
        }
    };

    const handleCreateSprint = async (e) => {
        e.preventDefault();

        if (sprintData.start_date > sprintData.end_date) {
            showNotification("Start date cannot be greater than end date.", "error");
            return;
        }

        try {
            await createSprint({
                name: sprintData.name,
                project_id: sprintData.project_id,
                created_by: user.user_id,
                start_date: sprintData.start_date,
                end_date: sprintData.end_date,
            });
            await loadSprints();
            showNotification("Sprint created successfully.", "success");
            setShowCreateModal(false);

            setSprintData({
                name: "",
                project_id: projects[0]?.project_id || "",
                start_date: "",
                end_date: "",
            });
            setPage(1);

        } catch (error) {
            showNotification(error.detail || "Sprint creation failed.", "error");
        }
    };
    const handleStartSprint = async () => {
        try {
            await startSprint(selectedSprint.sprint_id, {
                updated_by: user.user_id,
            });

            showNotification("Sprint started successfully.", "success");
            await loadSprints();

            setSelectedSprint({
                ...selectedSprint,
                status: "active",
            });
        } catch (error) {
            showNotification(error.detail || "Failed to start sprint.", "error");
        }
    };
    const handleCompleteSprint = async () => {
        try {
            await completeSprint(selectedSprint.sprint_id, {
                updated_by: user.user_id,
            });

            showNotification("Sprint completed successfully.", "success");
            await loadSprints();

            setSelectedSprint({
                ...selectedSprint,
                status: "completed",
            });
        } catch (error) {
            showNotification(error.detail || "Failed to complete sprint.", "error");
        }
    };
    const handleRemoveIssueFromSprint = async (issueId) => {
        try {
            await removeIssueFromSprint(selectedSprint.sprint_id, {
                issue_id: issueId,
            });

            showNotification("Issue removed successfully.", "success");
            await loadSprints();

            setSelectedSprint((prev) => ({
                ...prev,
                issues: prev.issues.filter((issue) => issue.issue_id !== issueId),
            }));
        } catch (error) {
            showNotification(error.detail || "Failed to remove issue.", "error");
        }
    };

    return (
        <div className="dashboard-layout">
            <Sidebar />

            <main className="dashboard-main">
                {!selectedSprint ? (
                    <SprintList
                        user={user}
                        projects={projects}
                        sprints={sprints}
                        selectedProjectId={selectedProjectId}
                        setSelectedProjectId={setSelectedProjectId}
                        statusFilter={statusFilter}
                        setStatusFilter={setStatusFilter}
                        search={search}
                        setSearch={setSearch}
                        page={page}
                        setPage={setPage}
                        totalPages={totalPages}
                        setSelectedSprint={setSelectedSprint}
                        loadAvailableIssues={loadAvailableIssues}
                        showCreateModal={showCreateModal}
                        setShowCreateModal={setShowCreateModal}
                        sprintData={sprintData}
                        setSprintData={setSprintData}
                        handleCreateSprint={handleCreateSprint}
                    />
                ) : (
                    <SprintDetail
                        user={user}
                        selectedSprint={selectedSprint}
                        setSelectedSprint={setSelectedSprint}
                        availableIssues={availableIssues}
                        selectedIssueId={selectedIssueId}
                        setSelectedIssueId={setSelectedIssueId}
                        handleAddIssueToSprint={handleAddIssueToSprint}
                        handleStartSprint={handleStartSprint}
                        handleCompleteSprint={handleCompleteSprint}
                        handleRemoveIssueFromSprint={handleRemoveIssueFromSprint}
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

export default Sprint;
