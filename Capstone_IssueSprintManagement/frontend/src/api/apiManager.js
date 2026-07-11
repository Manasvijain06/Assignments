import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use(
  (config) => {
    const storedUser = JSON.parse(
      localStorage.getItem("user") || "{}"
    );

    if (storedUser.access_token) {
      config.headers.Authorization =
        `Bearer ${storedUser.access_token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

const handleError = (error) => {
  throw (
    error.response?.data || {
      detail: "Something went wrong.",
    }
  );
};

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

// PATCH
export const _patch = async (url, data) => {
    try {
        const response = await api.patch(url, data);
        return response.data;
    } catch (error) {
        throw error.response?.data || {
            detail: "Something went wrong.",
        };
    }
};