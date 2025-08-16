import axios from "axios";
import Cookies from "js-cookie";

const BASE_URL = "https://localhost:8000/";

// Helper functions to read from cookies
const getAccessToken = () => Cookies.get("accessToken");
const getRefreshToken = () => Cookies.get("refreshToken");

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // if backend uses cookies with httpOnly or same-site policy
});

// --- REQUEST INTERCEPTOR ---
api.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// --- RESPONSE INTERCEPTOR (Handles token refresh) ---
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = getRefreshToken();
        if (!refreshToken) throw new Error("No refresh token available");

        const { data } = await axios.post(
          `${BASE_URL}api/token/refresh/`,
          { refresh: refreshToken },
          {
            headers: {
              "Content-Type": "application/json",
            },
            withCredentials: true,
          }
        );

        // Save new accessToken in cookies
        Cookies.set("accessToken", data.access, {
          expires: 1,
          sameSite: "Strict",
          secure: process.env.NODE_ENV === "production",
        });

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        Cookies.remove("accessToken");
        Cookies.remove("refreshToken");
        Cookies.remove("isSigned");
        localStorage.removeItem("isSigned");
        window.location.href = "/auth/login";
      }
    }

    return Promise.reject(error);
  }
);

export default api;
