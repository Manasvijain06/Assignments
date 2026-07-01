import { _post, _get, _put, _delete } from "../api/apiManager";

export const registerUser = async (userData) => {
    return _post("auth/register", userData);
};

export const loginUser = async (userData) => {
    return _post("/auth/login", userData);
};

export const getUsersByRole = async (role) => {
    return _get(`/users/by-role?role=${role}`);
};

export const createProject = async (adminEmail, projectData) => {
    return _post(`/projects/?admin_email=${adminEmail}`, projectData);
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