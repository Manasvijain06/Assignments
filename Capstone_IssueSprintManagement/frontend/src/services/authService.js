import { _post } from "../api/apiManager";

export const registerUser = async (userData) => {
    return _post(
    "auth/register",
    userData
    );
};