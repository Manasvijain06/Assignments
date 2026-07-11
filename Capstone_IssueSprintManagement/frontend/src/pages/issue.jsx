import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import IssueList from "../components/issues/IssueList";
import IssueDetail from "../components/issues/IssueDetail";
import Notification from "../components/Notification";

import {
    createIssue,
    getProjectIssues,
    getProjects,
    updateIssueStatus,
    getProjectStories,
    addIssueComment,
    updateIssueComment,
    deleteIssueComment,
} from "../services/auth-service";

const initialFilters = {
  status: "all",
  priority: "all",
  assignee: "all",
  search: "",
};

const initialIssueData = {
  title: "",
  description: "",
  type: "task",
  priority: "medium",
  assignee: "",
  parent_id: "",
};

function Issue() {
    const user = JSON.parse(localStorage.getItem("user") || "{}");

    const [projects, setProjects] = useState([]);
    const [selectedProjectId, setSelectedProjectId] = useState(
        localStorage.getItem("selectedProjectId") || ""
    );

    const [issues, setIssues] = useState([]);
    const [members, setMembers] = useState([]);
    const [stories, setStories] = useState([]);
    const [selectedIssue, setSelectedIssue] = useState(null);

    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const limit = 6;

    const [filters, setFilters] = useState(initialFilters);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [issueData, setIssueData] = useState(initialIssueData);

    const [errors, setErrors] = useState({
      title: "",
      description: "",
    });

    const [commentText, setCommentText] = useState("");
    const [editingCommentId, setEditingCommentId] = useState(null);
    const [editCommentText, setEditCommentText] = useState("");

    const [notification, setNotification] = useState({
        message: "",
        type: "",
    });

    useEffect(() => {
      loadProjects();
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

    const showNotification = (message, type = "success") => {
        setNotification({ message, type });

        setTimeout(() => {
            setNotification({ message: "", type: "" });
        }, 3000);
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
          await loadStories(savedProjectId);
        } else if (visibleProjects.length > 0) {
          const firstProjectId = visibleProjects[0].project_id;

          setSelectedProjectId(firstProjectId);
          localStorage.setItem("selectedProjectId", firstProjectId);

          await loadStories(firstProjectId);
        } else {
          setSelectedProjectId("");
          setIssues([]);
          setStories([]);
          localStorage.removeItem("selectedProjectId");
        }
      } catch (error) {
        showNotification(error.detail || "Failed to load projects.", "error");
      }
    };
    useEffect(() => {
      const selectedProject = projects.find(
        (project) => project.project_id === selectedProjectId,
      );

      const projectMembers = (selectedProject?.members || []).filter(
        (member) => member.role === "member",
      );

      setMembers(projectMembers);
    }, [projects, selectedProjectId]);

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
    };

    const handleCloseCreateModal = () => {
      setShowCreateModal(false);

      setErrors({
        title: "",
        description: "",
      });

      setIssueData(initialIssueData);
    };

    const handleCreateIssue = async (e) => {
        e.preventDefault();

         const newErrors = {
           title: "",
           description: "",
           assignee: "",
         };

         if (!issueData.title.trim()) {
           newErrors.title = "Title is required.";
         }

         if (!issueData.description.trim()) {
           newErrors.description = "Description is required.";
         }

         if (!issueData.assignee) {
           newErrors.assignee = "Assignee is required.";
         }

          if (newErrors.title || newErrors.description || newErrors.assignee) {
            setErrors(newErrors);
            return;
          }

          setErrors({
            title: "",
            description: "",
            assignee: "",
          });

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
            setIssueData(initialIssueData);

            await loadIssues();
        } catch (error) {
            showNotification(error.detail || "Issue creation failed.", "error");
        }
    };

    const refreshSelectedIssue = async () => {
        const response = await getProjectIssues(selectedProjectId, {
            page,
            limit,
            status: filters.status,
            priority: filters.priority,
            assignee: filters.assignee,
            search: filters.search,
        });

        setIssues(response.items);

        const allIssues = response.items.flatMap((issue) => [
            issue,
            ...(issue.children || []),
        ]);

        const updatedIssue = allIssues.find(
            (issue) => issue.issue_id === selectedIssue.issue_id,
        );

        if (updatedIssue) {
            setSelectedIssue(updatedIssue);
        }
    };

    const handleAddComment = async () => {
        if (!commentText.trim()){
            showNotification("Comment cannot be empty.","error")
            return;
        }

        try {
            await addIssueComment(selectedIssue.issue_id, {
                user_id: user.user_id,
                comment: commentText,
            });

            setCommentText("");
            showNotification("Comment added successfully.", "success");

            await refreshSelectedIssue();
        } catch (error) {
            showNotification(error.detail || "Failed to add comments.", "error");
        }
    };

    const handleEditComment = (comment) => {
        setEditingCommentId(comment.comment_id);
        setEditCommentText(comment.comment);
    };

    const handleUpdateComment = async (commentId) => {
        try {
            await updateIssueComment(selectedIssue.issue_id, commentId, {
                user_id: user.user_id,
                comment: editCommentText,
            });

            setEditingCommentId(null);
            setEditCommentText("");

            showNotification("Comment updated successfully.", "success");
            await refreshSelectedIssue();
        } catch (error) {
            showNotification(error.detail || "Failed to update comment.","error",
            );
        }
    };

    const handleDeleteComment = async (commentId) => {
        try {
            await deleteIssueComment(
                selectedIssue.issue_id,
                commentId,
                user.user_id,
            );
            showNotification("Comment deleted successfully.", "success");
            await refreshSelectedIssue();
        } catch (error) {
            showNotification(error.detail || "Failed to delete comment.", "error");
        }
    };


    const canUpdateStatus = (issue) => {
      if (!user) return false;

      return (
        user.role === "admin" ||
        (user.role === "member" && issue.assignee?.user_id === user.user_id)
      );
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
    const loadStories = async (projectId) => {
      try {
        const data = await getProjectStories(projectId);
        setStories(data);
      } catch (error) {
        showNotification(error.detail || "Failed to load stories.", "error");
      }
    };

    return (
      <div className="dashboard-layout">
        <Sidebar />

        <main className="dashboard-main">
          {!selectedIssue ? (
            <IssueList
              user={user}
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
              errors={errors}
              setErrors={setErrors}
              handleCloseCreateModal={handleCloseCreateModal}
            />
          ) : (
            <IssueDetail
              selectedIssue={selectedIssue}
              setSelectedIssue={setSelectedIssue}
              canUpdateStatus={canUpdateStatus}
              handleDetailStatusChange={handleDetailStatusChange}
              user={user}
              commentText={commentText}
              setCommentText={setCommentText}
              editingCommentId={editingCommentId}
              editCommentText={editCommentText}
              setEditCommentText={setEditCommentText}
              handleAddComment={handleAddComment}
              handleEditComment={handleEditComment}
              handleUpdateComment={handleUpdateComment}
              handleDeleteComment={handleDeleteComment}
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

