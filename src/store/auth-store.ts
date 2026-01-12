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
  const [hasHydrated, setHasHydrated] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (!isClient) {
      return;
    }
    const persist = useAuthStore.persist;
    if (!persist) {
      setHasHydrated(true);
      return;
    }

    const unsubFinish = persist.onFinishHydration?.(() => setHasHydrated(true));
    const hydrated = persist.hasHydrated?.() ?? false;

    if (hydrated) {
      setHasHydrated(true);
    }

    return () => {
      unsubFinish?.();
    };
  }, [isClient]);

  return isClient && hasHydrated;
};

export const useAuthSelector = <T>(selector: (state: IAuthStore) => T) =>
  useAuthStore(selector);
