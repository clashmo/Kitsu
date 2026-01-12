"use client";

import { useStore } from "zustand";
import type { StoreApi, UseBoundStore } from "zustand";

type Selector<TState, TSlice> = (state: TState) => TSlice;
type EqualityChecker<TSlice> = (a: TSlice, b: TSlice) => boolean;

type BoundStore<TState> = UseBoundStore<StoreApi<TState>> & {
  persist?: unknown;
};

export const createStoreFactory = <TState extends object>(
  initializer: () => BoundStore<TState>,
) => {
  let clientStore: BoundStore<TState> | null = null;

  const getStore = () => {
    if (typeof window === "undefined") {
      return initializer();
    }

    if (!clientStore) {
      clientStore = initializer();
    }

    return clientStore;
  };

  const identitySelector = (state: TState) => state;

  function useBoundStoreBase(): TState;
  function useBoundStoreBase<StateSlice>(
    selector: Selector<TState, StateSlice>,
    equalityFn?: EqualityChecker<StateSlice>,
  ): StateSlice;
  function useBoundStoreBase<StateSlice>(
    selector: Selector<TState, StateSlice> = identitySelector as Selector<
      TState,
      StateSlice
    >,
    equalityFn?: EqualityChecker<StateSlice>,
  ) {
    const store = getStore();
    return useStore(store, selector, equalityFn);
  }

  const useBoundStore = useBoundStoreBase as BoundStore<TState>;

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
      get: () => getStore().persist,
    },
  });

  return { getStore, useBoundStore };
};
