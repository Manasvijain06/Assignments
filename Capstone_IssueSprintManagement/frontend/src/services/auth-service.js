import { _post } from "../api/apiManager";

export const registerUser = async (userData) => {
    return axios.post(
    "auth/register",
    userData
    );
};

export const loginUser = async (userData) => {
    return axios.post(
    "auth/login",
    userData
    );
};