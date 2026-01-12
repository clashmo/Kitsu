"use client";

import { useStore } from "zustand";
import type { StoreApi, UseBoundStore } from "zustand";

type Selector<TState, TSlice> = (state: TState) => TSlice;
type EqualityChecker<TSlice> = (a: TSlice, b: TSlice) => boolean;

export const createStoreFactory = <TState extends object>(
  initializer: () => UseBoundStore<StoreApi<TState>>,
) => {
  let clientStore: UseBoundStore<StoreApi<TState>> | null = null;

  const getStore = () => {
    if (typeof window === "undefined") {
      return initializer();
    }

    if (!clientStore) {
      clientStore = initializer();
    }

    return clientStore;
  };

  const useBoundStore = (<StateSlice>(
    selector?: Selector<TState, StateSlice>,
    equalityFn?: EqualityChecker<StateSlice>,
  ) => useStore(getStore(), selector as any, equalityFn)) as UseBoundStore<
    StoreApi<TState>
  >;

  Object.defineProperties(useBoundStore, {
    getState: {
      get: () => getStore().getState,
    },
    setState: {
      get: () => getStore().setState,
    },
    subscribe: {
      get: () => getStore().subscribe,
    },
    destroy: {
      get: () => getStore().destroy,
    },
    persist: {
      get: () => (getStore() as unknown as { persist?: unknown }).persist,
    },
  });

  return { getStore, useBoundStore };
};

