"use client";

import { useEffect, useState } from "react";
import { create } from "zustand";
import { persist } from "zustand/middleware";

export type IAuth = {
  id?: string;
  avatar?: string;
  email?: string;
  username?: string;
  collectionId?: string;
  collectionName?: string;
  autoSkip?: boolean;
  accessToken: string;
  refreshToken: string;
};

export interface IAuthStore {
  auth: IAuth | null;
  setAuth: (state: IAuth) => void;
  clearAuth: () => void;
  isRefreshing: boolean;
  setIsRefreshing: (val: boolean) => void;
  isAuthReady: boolean;
  setIsAuthReady: (val: boolean) => void;
}

export const useAuthStore = create<IAuthStore>()(
  persist(
    (set) => ({
      auth: null,
      setAuth: (state: IAuth) => set({ auth: state }),
      clearAuth: () => set({ auth: null }),
      isRefreshing: false,
      setIsRefreshing: (val: boolean) => set({ isRefreshing: val }),
      isAuthReady: false,
      setIsAuthReady: (val: boolean) => set({ isAuthReady: val }),
    }),
    {
      name: "auth",
      partialize: (state) => ({
        auth: state.auth,
      }),
      version: 0,
    },
  ),
);

export const useAuthHydrated = () => {
  const [isClient, setIsClient] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (!isClient) {
      return;
    }

    const persist = useAuthStore.persist;
    if (!persist) {
      setHydrated(true);
      return;
    }

    if (persist.hasHydrated?.()) {
      setHydrated(true);
      return;
    }

    const unsub = persist.onFinishHydration?.(() => setHydrated(true));

    return () => {
      unsub?.();
    };
  }, [isClient]);

  return isClient && hydrated;
};

export const useAuthSelector = <T>(selector: (state: IAuthStore) => T) =>
  useAuthStore(selector);
