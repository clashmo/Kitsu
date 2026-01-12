"use client";

import { useEffect, useRef } from "react";
import { api, refreshSession } from "@/lib/api";
import {
  useAuthHydrated,
  useAuthSelector,
  useAuthStore,
} from "@/store/auth-store";

type ProfileResponse = {
  id?: string;
  email?: string;
};

const AuthBootstrap = () => {
  const auth = useAuthSelector((state) => state.auth);
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
        // Refresh must complete before fetching the profile to avoid unauthorized responses.
        const profile = await api.get<ProfileResponse>("/users/me");
        if (cancelled) return;
        useAuthStore.setState((state) => {
          if (!state.auth) return state;
          const email = profile.data?.email ?? state.auth.email;
          const username = email ? email.split("@")[0] : state.auth.username;
          return {
            auth: {
              ...state.auth,
              id: profile.data?.id ?? state.auth.id,
              email,
              username,
              accessToken: newToken || state.auth.accessToken,
              refreshToken: state.auth.refreshToken,
            },
          };
        });
      } catch (error) {
        if (!cancelled) {
          // eslint-disable-next-line no-console
          console.warn("[auth] bootstrap failed", error);
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
