import { FiArrowLeft } from "react-icons/fi";

function IssueDetail({
    selectedIssue,
    setSelectedIssue,
    canUpdateStatus,
    handleDetailStatusChange,
}) {
    return (
        <>
            <div className="back-link" onClick={() => setSelectedIssue(null)}>
                <FiArrowLeft size={15} />
                <span>Back</span>
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
