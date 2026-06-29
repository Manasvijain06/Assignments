import { _post } from "../api/apiManager";

export const registerUser = async (userData) => {
    return axios.post(
    `${API_URL}/register`,
    userData
    );
};