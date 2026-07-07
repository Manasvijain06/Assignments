import { FiArrowLeft } from "react-icons/fi";

function SprintDetail({
    selectedSprint,
    setSelectedSprint,
    availableIssues,
    selectedIssueId,
    setSelectedIssueId,
    handleAddIssueToSprint,
}) {
    return (
        <>
            <div className="back-link" onClick={() => setSelectedSprint(null)}>
                <FiArrowLeft size={15} />
                <span>Back</span>
            </div>

            <div className="issue-detail-page">
                <div className="issue-detail-main">
                    <div className="issue-detail-title-card">
                        <div className="issue-key-badge">{selectedSprint.status}</div>

                        <h1>{selectedSprint.name}</h1>

                        <div className="issue-meta-row">
                            <span className={`sprint-status ${selectedSprint.status}`}>
                                {selectedSprint.status}
                            </span>
                        </div>
                    </div>

                    <div className="issue-detail-section">
                        <h3>Progress</h3>
                        <div className="sprint-progress-cell">
                            <div className="sprint-progress-bar">
                                <div
                                    className="sprint-progress-fill"
                                    style={{ width: `${selectedSprint.progress}%` }}
                                />
                            </div>
                            <span>{selectedSprint.progress}%</span>
                        </div>
                    </div>

                    <div className="issue-detail-section">
                        <h3>Issues in Sprint</h3>

                        {selectedSprint.issues?.length > 0 ? (
                            selectedSprint.issues.map((issue) => (
                                <div className="child-detail-row" key={issue.issue_id}>
                                    <div>
                                        <strong>{issue.issue_key}</strong>
                                    </div>

                                    <div>{issue.title}</div>

                                    <span className={`type-badge ${issue.type}`}>
                                        {issue.type}
                                    </span>

                                    <span className={`status-badge ${issue.status}`}>
                                        {issue.status.replace("_", " ").toUpperCase()}
                                    </span>
                                </div>
                            ))
                        ) : (
                            <p className="empty-text">No issues added.</p>
                        )}
                    </div>
                </div>

                <div className="issue-detail-sidebar">
                    <h3>Details</h3>

                    <div className="detail-field">
                        <label>Status</label>
                        <p>{selectedSprint.status.toUpperCase()}</p>
                    </div>

                    <div className="detail-field">
                        <label>Start Date</label>
                        <p>{selectedSprint.start_date}</p>
                    </div>

                    <div className="detail-field">
                        <label>End Date</label>
                        <p>{selectedSprint.end_date}</p>
                    </div>

                    <div className="detail-field">
                        <label>Issues</label>
                        <p>
                            {selectedSprint.completed_issues}/{selectedSprint.total_issues}
                        </p>
                    </div>

                    <div className="detail-field">
                        <label>Add Issue</label>

                        <select
                            value={selectedIssueId}
                            onChange={(e) => setSelectedIssueId(e.target.value)}
                        >
                            <option value="">Select issue</option>

                            {availableIssues.map((issue) => (
                                <option key={issue.issue_id} value={issue.issue_id}>
                                    {issue.issue_key} - {issue.title}
                                </option>
                            ))}
                        </select>

                        <button
                            className="modal-create-btn"
                            type="button"
                            onClick={handleAddIssueToSprint}
                        >
                            Add Issue
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
}

export default SprintDetail;
