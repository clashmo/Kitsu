import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import { env } from "next-runtime-env";
import { useAuthStore } from "@/store/auth-store";

const baseURL = env("NEXT_PUBLIC_API_URL") || "";

export const api = axios.create({
  baseURL,
});

const authClient = axios.create({
  baseURL,
});

type TokenPayload = {
  access_token?: string;
  accessToken?: string;
  token?: string;
  refresh_token?: string;
  refreshToken?: string;
};

let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value?: unknown) => void;
  reject: (error: unknown) => void;
}> = [];

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error);
    } else {
      promise.resolve(token);
    }
  });
  failedQueue = [];
};

const extractTokens = (payload: TokenPayload) => {
  const accessToken =
    payload?.access_token ||
    payload?.accessToken ||
    payload?.token ||
    "";
  const refreshToken =
    payload?.refresh_token ||
    payload?.refreshToken ||
    "";
  return { accessToken, refreshToken };
};

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = useAuthStore.getState().auth?.accessToken;
  if (token) {
    // eslint-disable-next-line no-param-reassign
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    };

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = useAuthStore.getState().auth?.refreshToken;

      if (!refreshToken) {
        useAuthStore.getState().clearAuth();
        return Promise.reject(error);
      }

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            if (token && originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${token}`;
            }
            return api(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      isRefreshing = true;

      try {
        const { data } = await authClient.post("/auth/refresh", {
          refresh_token: refreshToken,
        });
        const tokens = extractTokens(data as TokenPayload);
        if (!tokens.accessToken && useAuthStore.getState().auth?.accessToken) {
          // eslint-disable-next-line no-console
          console.warn("Using existing access token because refresh returned none");
        }
        const updatedAuth = useAuthStore.getState().auth;
        if (updatedAuth) {
          useAuthStore
            .getState()
            .setAuth({
              ...updatedAuth,
              accessToken: tokens.accessToken,
              refreshToken: tokens.refreshToken,
            });
        }
        // Prefer freshly issued token; fall back to stored token if backend omitted it
        const newToken = tokens.accessToken || useAuthStore.getState().auth?.accessToken || null;
        if (!newToken) {
          processQueue(new Error("No token returned from refresh"), null);
          useAuthStore.getState().clearAuth();
          return Promise.reject(new Error("No token returned from refresh"));
        }
        processQueue(null, newToken);
        if (originalRequest.headers && newToken) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
        }
        return api(originalRequest);
      } catch (err) {
        processQueue(err, null);
        useAuthStore.getState().clearAuth();
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  },
);
