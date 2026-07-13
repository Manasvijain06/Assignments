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
} from "../services/auth-service";

function Sprint() {
    const user = JSON.parse(localStorage.getItem("user"));

    const [projects, setProjects] = useState([]);
    const [sprints, setSprints] = useState([]);

    const [selectedProjectId, setSelectedProjectId] = useState("all");
    const [statusFilter, setStatusFilter] = useState("all");
    const [search, setSearch] = useState("");

    const [selectedSprint, setSelectedSprint] = useState(null);
    const [availableIssues, setAvailableIssues] = useState([]);
    const [selectedIssueId, setSelectedIssueId] = useState("");

    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const limit = 6;

    const [showCreateModal, setShowCreateModal] = useState(false);

    const [notification, setNotification] = useState({
        message: "",
        type: "",
    });

    const showNotification = (message, type = "success") => {
        setNotification({ message, type });

        setTimeout(() => {
            setNotification({ message: "", type: "" });
        }, 3000);
    };
    const [sprintData, setSprintData] = useState({
        name: "",
        project_id: "",
        start_date: "",
        end_date: "",
    });

    useEffect(() => {
        loadProjects();
    }, []);

    useEffect(() => {
        loadSprints();
    }, [page, selectedProjectId, statusFilter, search]);

    const loadProjects = async () => {
        try {
            const data = await getProjects();
            setProjects(data);

            if (data.length > 0) {
                setSprintData((prev) => ({
                    ...prev,
                    project_id: data[0].project_id,
                }));
            }
        } catch (error) {
            showNotification(error.detail || "Failed to load projects.", "error");
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

    const loadAvailableIssues = async (projectId) => {
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

            setAvailableIssues(
                allIssues.filter((issue) => issue.status !== "done"),
            );
        } catch (error) {
            showNotification(error.detail || "Failed to load issues.", "error");
        }
    };

    const handleAddIssueToSprint = async () => {
        if (!selectedIssueId) return;

        try {
            await addIssueToSprint(selectedSprint.sprint_id, {
                issue_id: selectedIssueId,
            });

            showNotification("Issue added to sprint.", "success");

            setSelectedIssueId("");
            await loadSprints();

            const updated = sprints.find(
                (sprint) => sprint.sprint_id === selectedSprint.sprint_id,
            );

            if (updated) {
                setSelectedSprint(updated);
            }
        } catch (error) {
            showNotification(error.detail || "Failed to add issue.", "error");
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

            showNotification("Sprint created successfully.", "success");
            setShowCreateModal(false);

            setSprintData({
                name: "",
                project_id: projects[0]?.project_id || "",
                start_date: "",
                end_date: "",
            });
            setPage(1);
            await loadSprints();
        } catch (error) {
            showNotification(error.detail || "Sprint creation failed.", "error");
        }
    };

    return (
        <div className="dashboard-layout">
            <Sidebar />

            <main className="dashboard-main">
                {!selectedSprint ? (
                    <SprintList
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
                        selectedSprint={selectedSprint}
                        setSelectedSprint={setSelectedSprint}
                        availableIssues={availableIssues}
                        selectedIssueId={selectedIssueId}
                        setSelectedIssueId={setSelectedIssueId}
                        handleAddIssueToSprint={handleAddIssueToSprint}
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
