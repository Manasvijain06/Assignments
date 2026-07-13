import { useState } from "react";

function IssueDetail({
  selectedIssue,
  setSelectedIssue,
  canUpdateStatus,
  handleDetailStatusChange,
  user,
  commentText,
  setCommentText,
  editingCommentId,
  editCommentText,
  setEditCommentText,
  handleAddComment,
  handleEditComment,
  handleUpdateComment,
  handleDeleteComment,
}) {
  const [commentPage, setCommentPage] = useState(1);
  const commentsPerPage = 3;

  const comments = selectedIssue.comments || [];
  const children = selectedIssue.children || [];
  const totalCommentPages =
    Math.ceil(comments.length / commentsPerPage) || 1;

  const paginatedComments = comments.slice(
    (commentPage - 1) * commentsPerPage,
    commentPage * commentsPerPage,
  );

  return (
    <>
      <div className="back-link" onClick={() => setSelectedIssue(null)}>
        <span className="back-arrow">← Back</span>
      </div>

      <div className="issue-detail-page">
        <div className="issue-detail-main">
          <div className="issue-detail-title-card">
            <div className="issue-key-badge">{selectedIssue.issue_key}</div>

            <h1>{selectedIssue.title}</h1>

            <div className="issue-meta-row">
              <span className={`type-badge ${selectedIssue.type}`}>
                {selectedIssue.type}
              </span>

              <span className={`priority-badge ${selectedIssue.priority}`}>
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
            <div className="comments-header">
              <h3>Comments</h3>
            </div>

            {user?.role !== "viewer" && (
            <div className="comment-input-box">
              <textarea
                placeholder="Write a comment..."
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
              />

              <button
                type="button"
                className="modal-create-btn"
                onClick={handleAddComment}
              >
                Add Comment
              </button>
            </div>
            )}

            <div className="comments-list">
              {comments.length > commentsPerPage && (
                <div className="pagination">
                  <button
                    type="button"
                    disabled={commentPage === 1}
                    onClick={() => setCommentPage((prev) => prev - 1)}
                  >
                    ‹
                  </button>

                  {[...Array(totalCommentPages)].map((_, index) => (
                    <button
                      type="button"
                      key={index + 1}
                      className={commentPage === index + 1 ? "active-page" : ""}
                      onClick={() => setCommentPage(index + 1)}
                    >
                      {index + 1}
                    </button>
                  ))}

                  <button
                    type="button"
                    disabled={commentPage === totalCommentPages}
                    onClick={() => setCommentPage((prev) => prev + 1)}
                  >
                    ›
                  </button>
                </div>
              )}
              {(selectedIssue.comments || []).length === 0 ? (
                <p className="empty-text">No comments yet.</p>
              ) : (
                paginatedComments.map((comment) => (
                  <div className="comment-card" key={comment.comment_id}>
                    <div className="comment-top">
                      <div>
                        <strong>{comment.user?.name || "User"}</strong>
                        <span>
                          {comment.created_at
                            ? new Date(comment.created_at).toLocaleString()
                            : ""}
                        </span>
                      </div>

                      {comment.user?.user_id === user?.user_id && (
                        <div className="comment-actions">
                          <button
                            type="button"
                            onClick={() => handleEditComment(comment)}
                          >
                            Edit
                          </button>

                          <button
                            type="button"
                            onClick={() =>
                              handleDeleteComment(comment.comment_id)
                            }
                          >
                            Delete
                          </button>
                        </div>
                      )}
                    </div>

                    {editingCommentId === comment.comment_id ? (
                      <div className="comment-edit-box">
                        <textarea
                          value={editCommentText}
                          onChange={(e) => setEditCommentText(e.target.value)}
                        />

                        <button
                          type="button"
                          className="modal-create-btn"
                          onClick={() =>
                            handleUpdateComment(comment.comment_id)
                          }
                        >
                          Save
                        </button>
                      </div>
                    ) : (
                      <p>{comment.comment}</p>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        <div className="issue-detail-sidebar">
          <h3>Details</h3>

          <div className="detail-field">
            <label>Status</label>

            {canUpdateStatus(selectedIssue) ? (
              <select
                value={selectedIssue.status}
                onChange={(e) => handleDetailStatusChange(e.target.value)}
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

          <div className="issue-detail-actions"></div>
        </div>
      </div>
    </>
  );
}

export default IssueDetail;
