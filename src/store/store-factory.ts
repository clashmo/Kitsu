"use client";

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

  const useBoundStore = Object.assign(
    function useBoundStoreBase<StateSlice = TState>(
      selector?: Selector<TState, StateSlice>,
      equalityFn?: EqualityChecker<StateSlice>,
    ) {
      const store = getStore();
      return selector
        ? store(selector, equalityFn)
        : store();
    },
    {
      getState: () => getStore().getState(),
      setState: (
        ...args: Parameters<BoundStore<TState>["setState"]>
      ) => getStore().setState(...args),
      subscribe: (
        ...args: Parameters<BoundStore<TState>["subscribe"]>
      ) => getStore().subscribe(...args),
      destroy: () => getStore().destroy(),
      get persist() {
        return getStore().persist;
      },
    },
  ) satisfies BoundStore<TState>;

  return { getStore, useBoundStore };
};
