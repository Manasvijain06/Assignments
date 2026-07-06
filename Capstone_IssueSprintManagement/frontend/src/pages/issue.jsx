import React, { useEffect, useState } from "react";
import { FiArrowLeft } from "react-icons/fi";
import Sidebar from "../components/Sidebar";
import {
    createIssue,
    getProjectIssues,
    getProjects,
    getUsersByRole,
    updateIssueStatus,
    getProjectStories
} from "../services/auth-service";
import { toast } from "react-toastify";

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
            toast.error(error.detail || "Failed to load projects.");
        }
    };

    const loadUsers = async () => {
        try {
            const membersData = await getUsersByRole("member");
            const viewersData = await getUsersByRole("viewer");

            setMembers([...membersData, ...viewersData]);
        } catch (error) {
            toast.error(error.detail || "Failed to load users.");
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
            toast.error(error.detail || "Failed to load issues.");
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

            toast.success("Issue created successfully.");
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
            toast.error(error.detail || "Issue creation failed.");
        }
    };

    const handleStatusChange = async (issue, newStatus) => {
        try {
            await updateIssueStatus(issue.issue_id, {
                status: newStatus,
                updated_by: user.user_id,
            });

            toast.success("Issue status updated successfully.");
            await loadIssues();
        } catch (error) {
            toast.error(error.detail || "Status update failed.");
        }
    };

    const loadStories = async (projectId) => {
        try {
            const data = await getProjectStories(projectId);
            setStories(data);
        } catch (error) {
            toast.error(error.detail || "Failed to load stories.");
        }
    };

    const canUpdateStatus = (issue) => {
        if (!user) return false;

        return user.role === "admin" || issue.assignee?.user_id === user.user_id;
    };

    const renderIssueRow = (issue, isChild = false) => (
        <tr key={issue.issue_id} className={isChild ? "child-issue-row" : ""}>
            <td>{issue.issue_key}</td>

            <td
                className={`clickable-issue-title ${isChild ? "child-title" : ""}`}
                onClick={() => setSelectedIssue(issue)}
            >
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

            toast.success("Issue status updated successfully.");

            setSelectedIssue({
                ...selectedIssue,
                status: newStatus,
            });

            await loadIssues();
        } catch (error) {
            toast.error(error.detail || "Status update failed.");
        }
    };

    return (
        <div className="dashboard-layout">
            <Sidebar />

            <main className="dashboard-main">
                {!selectedIssue ? (
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
                                        setSelectedProjectId(e.target.value);
                                        setPage(1);
                                        setIssues([]);
                                        loadStories(e.target.value);
                                    }}
                                >
                                    {projects.map((project) => (
                                        <option
                                            key={project.project_id}
                                            value={project.project_id}
                                        >
                                            {project.name}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div>
                                <label>Status</label>
                                <select
                                    value={filters.status}
                                    onChange={(e) => {
                                        setFilters({ ...filters, status: e.target.value });
                                        setPage(1);
                                    }}
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
                                    onChange={(e) => {
                                        setFilters({ ...filters, priority: e.target.value });
                                        setPage(1);
                                    }}
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
                                    onChange={(e) => {
                                        setFilters({ ...filters, assignee: e.target.value });
                                        setPage(1);
                                    }}
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
                                            <React.Fragment key={issue.issue_id}>
                                                {renderIssueRow(issue)}

                                                {issue.children?.map((child) =>
                                                    renderIssueRow(child, true),
                                                )}
                                            </React.Fragment>
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
                    </>
                ) : (
                    <>
                        <div className="back-link" onClick={() => setSelectedIssue(null)}>
                            <FiArrowLeft size={15} />
                            <span>Back</span>
                        </div>

                        <div className="issue-detail-page">
                            <div className="issue-detail-main">
                                <div className="issue-detail-title-card">
                                    <div className="issue-key-badge">
                                        {selectedIssue.issue_key}
                                    </div>

                                    <h1>{selectedIssue.title}</h1>

                                    <div className="issue-meta-row">
                                        <span className={`type-badge ${selectedIssue.type}`}>
                                            {selectedIssue.type}
                                        </span>

                                        <span
                                            className={`priority-badge ${selectedIssue.priority}`}
                                        >
                                            {selectedIssue.priority}
                                        </span>

                                        <span className={`status-badge ${selectedIssue.status}`}>
                                            {selectedIssue.status.replace("_", " ").toUpperCase()}
                                        </span>
                                    </div>
                                </div>

                                <div className="issue-detail-section">
                                    <h3>Description</h3>
                                    <p>{selectedIssue.description}</p>
                                </div>

                                {selectedIssue.type === "story" && (
                                    <div className="issue-detail-section">
                                        <h3>Child Issues</h3>

                                        {selectedIssue.children?.length > 0 ? (
                                            selectedIssue.children.map((child) => (
                                                <div
                                                    className="child-detail-row"
                                                    key={child.issue_id}
                                                    onClick={() => setSelectedIssue(child)}
                                                >
                                                    <div>
                                                        <strong>{child.issue_key}</strong>
                                                        <span>{child.title}</span>
                                                    </div>

                                                    <span className={`status-badge ${child.status}`}>
                                                        {child.status.replace("_", " ").toUpperCase()}
                                                    </span>
                                                </div>
                                            ))
                                        ) : (
                                            <p className="empty-text">No child issues.</p>
                                        )}
                                    </div>
                                )}

                                <div className="issue-detail-section">
                                    <h3>Comments</h3>
                                    <p className="empty-text">
                                        Comments will be added in next feature.
                                    </p>
                                </div>
                            </div>

                            <div className="issue-detail-sidebar">
                                <h3>Details</h3>

                                <div className="detail-field">
                                    <label>Status</label>

                                    {canUpdateStatus(selectedIssue) ? (
                                        <select
                                            value={selectedIssue.status}
                                            onChange={(e) =>
                                                handleDetailStatusChange(e.target.value)
                                            }
                                        >
                                            <option value="backlog">Backlog</option>
                                            <option value="todo">Todo</option>
                                            <option value="in_progress">In Progress</option>
                                            <option value="done">Done</option>
                                        </select>
                                    ) : (
                                        <span className={`status-badge ${selectedIssue.status}`}>
                                            {selectedIssue.status.replace("_", " ").toUpperCase()}
                                        </span>
                                    )}
                                </div>

                                <div className="detail-field">
                                    <label>Assignee</label>
                                    <p>{selectedIssue.assignee?.name || "Unassigned"}</p>
                                </div>

                                <div className="detail-field">
                                    <label>Created By</label>
                                    <p>{selectedIssue.created_by?.name || "-"}</p>
                                </div>

                                <div className="detail-field">
                                    <label>Parent Story</label>
                                    <p>
                                        {selectedIssue.parent_story
                                            ? `${selectedIssue.parent_story.issue_key} - ${selectedIssue.parent_story.title}`
                                            : "No Parent"}
                                    </p>
                                </div>

                                <div className="issue-detail-actions">
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
                                    setIssueData({ ...issueData, title: e.target.value })
                                }
                                placeholder="Enter issue title"
                            />

                            <label>Description</label>
                            <textarea
                                value={issueData.description}
                                onChange={(e) =>
                                    setIssueData({ ...issueData, description: e.target.value })
                                }
                                placeholder="Enter issue description"
                            />

                            <label>Priority</label>
                            <select
                                value={issueData.priority}
                                onChange={(e) =>
                                    setIssueData({ ...issueData, priority: e.target.value })
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
                                            setIssueData({
                                                ...issueData,
                                                parent_id: e.target.value,
                                            })
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
                                    setIssueData({ ...issueData, assignee: e.target.value })
                                }>
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
    );
}

export default Issue;
