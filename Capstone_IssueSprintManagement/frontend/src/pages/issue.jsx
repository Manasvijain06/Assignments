import React, { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import IssueList from "../components/issues/IssueList";
import IssueDetail from "../components/issues/IssueDetail";
import Notification from "../components/Notification";

import {
    createIssue,
    getProjectIssues,
    getProjects,
    getUsersByRole,
    updateIssueStatus,
    getProjectStories
} from "../services/auth-service";

function Issue() {
    const user = JSON.parse(localStorage.getItem("user"));

    const [projects, setProjects] = useState([]);
    const [selectedProjectId, setSelectedProjectId] = useState("");

    const [issues, setIssues] = useState([]);
    const [members, setMembers] = useState([]);

    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const limit = 6;

    const [stories, setStories] = useState([]);
    const [selectedIssue, setSelectedIssue] = useState(null);

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

    const [filters, setFilters] = useState({
        status: "all",
        priority: "all",
        assignee: "all",
        search: "",
    });

    const [showCreateModal, setShowCreateModal] = useState(false);

    const [issueData, setIssueData] = useState({
        title: "",
        description: "",
        type: "task",
        priority: "medium",
        assignee: "",
        parent_id: "",
    });

    useEffect(() => {
        loadProjects();
        loadUsers();
    }, []);

    useEffect(() => {
        if (selectedProjectId) {
            loadIssues();
        }
    }, [
        selectedProjectId,
        page,
        filters.status,
        filters.priority,
        filters.assignee,
        filters.search,
    ]);

    const loadProjects = async () => {
        try {
            const data = await getProjects();
            setProjects(data);

            if (data.length > 0) {
                setSelectedProjectId(data[0].project_id);
                loadStories(data[0].project_id);
            }
        } catch (error) {
            showNotification(error.detail || "Failed to load projects.", "error");
        }
    };

    const loadUsers = async () => {
        try {
            const membersData = await getUsersByRole("member");
            const viewersData = await getUsersByRole("viewer");

            setMembers([...membersData, ...viewersData]);
        } catch (error) {
            showNotification(error.detail || "Failed to load users.", "error");
        }
    };

    const loadIssues = async () => {
        try {
            const response = await getProjectIssues(selectedProjectId, {
                page,
                limit,
                status: filters.status,
                priority: filters.priority,
                assignee: filters.assignee,
                search: filters.search,
            });

            setIssues(response.items);
            setTotalPages(response.total_pages);
        } catch (error) {
            showNotification(error.detail || "Failed to load issues.", "error");
        }
    };

    const handleSearch = (e) => {
        e.preventDefault();
        setPage(1);
        loadIssues();
    };

    const handleCreateIssue = async (e) => {
        e.preventDefault();

        try {
            await createIssue(selectedProjectId, {
                title: issueData.title,
                description: issueData.description,
                type: issueData.type,
                priority: issueData.priority,
                assignee: issueData.assignee,
                created_by: user.user_id,
                parent_id: issueData.parent_id || null,
            });

            showNotification("Issue created successfully.", "success");
            setShowCreateModal(false);

            setIssueData({
                title: "",
                description: "",
                type: "task",
                priority: "medium",
                assignee: "",
                parent_id: "",
            });

            await loadIssues();
        } catch (error) {
            showNotification(error.detail || "Issue creation failed.", "error");
        }
    };


    const loadStories = async (projectId) => {
        try {
            const data = await getProjectStories(projectId);
            setStories(data);
        } catch (error) {
            showNotification(error.detail || "Failed to load stories.", "error");
        }
    };

    const canUpdateStatus = (issue) => {
        if (!user) return false;

        return user.role === "admin" || issue.assignee?.user_id === user.user_id;
    };

    const renderIssueRow = (issue, isChild = false) => (
        <tr
            key={issue.issue_id}
            className={`${isChild ? "child-issue-row" : ""} clickable-row`}
            onClick={() => setSelectedIssue(issue)}
        >
            <td>{issue.issue_key}</td>

            <td className={isChild ? "child-title" : ""}>
                {isChild && <span className="tree-line">└─</span>}
                {issue.title}
            </td>

            <td>
                <span className={`type-badge ${issue.type}`}>{issue.type}</span>
            </td>

            <td>
                <span className={`priority-badge ${issue.priority}`}>
                    {issue.priority}
                </span>
            </td>

            <td>
                <span className={`status-badge ${issue.status}`}>
                    {issue.status.replace("_", " ").toUpperCase()}
                </span>
            </td>

            <td>{issue.assignee?.name || "Unassigned"}</td>
        </tr>
    );


    const handleDetailStatusChange = async (newStatus) => {
        try {
            await updateIssueStatus(selectedIssue.issue_id, {
                status: newStatus,
                updated_by: user.user_id,
            });

            showNotification("Issue status updated successfully.", "success");

            setSelectedIssue({
                ...selectedIssue,
                status: newStatus,
            });

            await loadIssues();
        } catch (error) {
            showNotification(error.detail || "Status update failed.", "error");
        }
    };

    return (
        <div className="dashboard-layout">
            <Sidebar />

            <main className="dashboard-main">
                {!selectedIssue ? (
                    <IssueList
                        projects={projects}
                        selectedProjectId={selectedProjectId}
                        setSelectedProjectId={setSelectedProjectId}
                        setPage={setPage}
                        setIssues={setIssues}
                        loadStories={loadStories}
                        filters={filters}
                        setFilters={setFilters}
                        members={members}
                        handleSearch={handleSearch}
                        issues={issues}
                        renderIssueRow={renderIssueRow}
                        page={page}
                        totalPages={totalPages}
                        showCreateModal={showCreateModal}
                        setShowCreateModal={setShowCreateModal}
                        issueData={issueData}
                        setIssueData={setIssueData}
                        handleCreateIssue={handleCreateIssue}
                        stories={stories}
                    />
                ) : (
                    <IssueDetail
                        selectedIssue={selectedIssue}
                        setSelectedIssue={setSelectedIssue}
                        canUpdateStatus={canUpdateStatus}
                        handleDetailStatusChange={handleDetailStatusChange}
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

export default Issue;

