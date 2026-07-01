import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

// GET
export const _get = async (url) => {
    try {
        const response = await api.get(url);
        return response.data;
    } catch (error) {
        throw error.response?.data || {
            detail: "Something went wrong.",
        };
    }
};

// POST
export const _post = async (url, data) => {
    try {
        const response = await api.post(url, data);
        return response.data;
    } catch (error) {
        throw error.response?.data || {
            detail: "Something went wrong.",
        };
    }
};

// PUT
export const _put = async (url, data) => {
    try {
        const response = await api.put(url, data);
        return response.data;
    } catch (error) {
        throw error.response?.data || {
            detail: "Something went wrong.",
        };
    }
};

// DELETE
export const _delete = async (url, data = {}) => {
    try {
        const response = await api.delete(url, { data });
        return response.data;
    } catch (error) {
        throw error.response?.data || {
            detail: "Something went wrong.",
        };
    }
};