"use client";

import { useEffect, useRef } from "react";
import { api, refreshSession } from "@/lib/api";
import {
  useAuthHydrated,
  useAuthSelector,
  useAuthStore,
} from "@/store/auth-store";

const AuthBootstrap = () => {
  const auth = useAuthSelector((state) => state.auth);
  const setAuth = useAuthSelector((state) => state.setAuth);
  const clearAuth = useAuthSelector((state) => state.clearAuth);
  const setIsAuthReady = useAuthSelector((state) => state.setIsAuthReady);
  const hydrated = useAuthHydrated();
  const initializedRef = useRef(false);

  useEffect(() => {
    if (!hydrated || initializedRef.current) {
      return;
    }
    initializedRef.current = true;
    let cancelled = false;

    const bootstrap = async () => {
      if (!auth?.refreshToken) {
        setIsAuthReady(true);
        return;
      }

      try {
        const newToken = await refreshSession(auth.refreshToken);
        const profile = await api.get("/users/me");
        if (cancelled) return;
        const currentAuth = useAuthStore.getState().auth || auth;
        if (currentAuth) {
          setAuth({
            ...currentAuth,
            id: (profile.data as any)?.id,
            email: (profile.data as any)?.email,
            username: (profile.data as any)?.email?.split("@")[0],
            accessToken: newToken || currentAuth.accessToken,
            refreshToken:
              useAuthStore.getState().auth?.refreshToken ||
              currentAuth.refreshToken,
          });
        }
      } catch {
        if (!cancelled) {
          clearAuth();
        }
      } finally {
        if (!cancelled) {
          setIsAuthReady(true);
        }
      }
    };

    bootstrap();

    return () => {
      cancelled = true;
    };
  }, [auth?.refreshToken, clearAuth, hydrated, setAuth, setIsAuthReady]);

  return null;
};

export default AuthBootstrap;
