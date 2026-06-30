import { _post } from "../api/apiManager";

export const registerUser = async (userData) => {
    return _post("auth/register", userData);
};

export const loginUser = async (userData) => {
    return _post("/auth/login", userData);
};