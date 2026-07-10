import { _delete, _get, _patch, _post, _put} from "../api/apiManager";

export const registerUser = async (userData) => {
    return _post("/auth/register", userData);
};

export const loginUser = async (userData) => {
    return _post("/auth/login", userData);
};

export const getUsersByRole = async (role) => {
    return _get(`/users/by-role?role=${role}`);
};

export const createProject = async (adminId, projectData) => {
    return _post(`/projects/?admin_id=${adminId}`, projectData);
};

export const addMemberToProject = async (projectId, memberData) => {
    return _post(`/projects/${projectId}/members`, memberData);
};

export const removeMemberFromProject = async (projectId, memberData) => {
    return _delete(`/projects/${projectId}/members`, memberData);
};

export const getProjects = async () => {
    return _get("/projects/");
};

export const updateProject = async (projectId, projectData) => {
    return _put(`/projects/${projectId}`, projectData);
};

export const deleteProject = async (projectId) => {
    return _delete(`/projects/${projectId}`);
};

export const createIssue = async (projectId, data) => {
    return _post(`/projects/${projectId}/issues`, data);
};

export const getProjectIssues = async (projectId, params = {}) => {
    const query = new URLSearchParams(params).toString();
    return _get(`/projects/${projectId}/issues?${query}`);
};

export const updateIssueStatus = async (issueId, data) => {
    return _patch(`/projects/issues/${issueId}/status`, data);
};

export const getProjectStories = async (projectId) => {
    return _get(`/projects/${projectId}/stories`);
};

export const createSprint = async (data) => {
    return _post("/sprints/", data);
};

export const startSprint = async (sprintId, data) => {
    return _patch(`/sprints/${sprintId}/start`, data);
};

export const completeSprint = async (sprintId, data) => {
    return _patch(`/sprints/${sprintId}/complete`, data);
};

export const addIssueToSprint = async (sprintId, data) => {
    return _post(`/sprints/${sprintId}/issues`, data);
};

export const removeIssueFromSprint = async (sprintId, data) => {
    return _delete(`/sprints/${sprintId}/issues`, data);
};

export const getSprints = async (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return _get(`/sprints/?${query}`);
};

export const updateProfile = async (userId, data) => {
    return _put(`/profile/${userId}`, data);
};

export const changePassword = async (userId, data) => {
    return _put(`/profile/${userId}/password`, data);
};

export const addIssueComment = async (issueId, data) => {
    return _post(`/projects/issues/${issueId}/comments`, data);
};

export const updateIssueComment = async (issueId, commentId, data) => {
    return _put(`/projects/issues/${issueId}/comments/${commentId}`, data);
};

export const deleteIssueComment = async (issueId, commentId, userId) => {
    return _delete(`/projects/issues/${issueId}/comments/${commentId}?user_id=${userId}`);
};