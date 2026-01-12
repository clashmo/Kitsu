import type { StoreApi, UseBoundStore } from "zustand";

type Selector<TState, TSlice> = (state: TState) => TSlice;
type EqualityChecker<TSlice> = (a: TSlice, b: TSlice) => boolean;

type BoundStore<TState> = UseBoundStore<StoreApi<TState>> & {
  persist?: {
    hasHydrated?: () => boolean;
    onFinishHydration?: (fn: () => void) => () => void;
  };
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

  function useBoundStoreBase(): TState;
  function useBoundStoreBase<StateSlice>(
    selector: Selector<TState, StateSlice>,
    equalityFn?: EqualityChecker<StateSlice>,
  ): StateSlice;
  function useBoundStoreBase<StateSlice = TState>(
    selector?: Selector<TState, StateSlice>,
    equalityFn?: EqualityChecker<StateSlice>,
  ) {
    const store = getStore();
    return selector !== undefined
      ? store(selector, equalityFn)
      : store();
  }

  const useBoundStore = Object.assign(
    useBoundStoreBase,
    {
      getState: () => getStore().getState(),
      setState: (
        ...args: Parameters<BoundStore<TState>["setState"]>
      ): ReturnType<BoundStore<TState>["setState"]> =>
        getStore().setState(...args),
      subscribe: (
        ...args: Parameters<BoundStore<TState>["subscribe"]>
      ) => getStore().subscribe(...args),
      destroy: () => getStore().destroy(),
      get persist() {
        const storePersist = getStore().persist;
        return storePersist ?? undefined;
      },
    },
  ) satisfies BoundStore<TState>;

  return { getStore, useBoundStore };
};
