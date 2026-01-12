import { create } from "zustand"
import { createStoreFactory } from "./store-factory"
import { IAnimeDetails } from "@/types/anime-details"

interface IAnimeStore {
    anime: IAnimeDetails,
    setAnime: (state: IAnimeDetails) => void
    selectedEpisode: string,
    setSelectedEpisode: (state: string) => void
}

const createAnimeStore = () => create<IAnimeStore>((set) => ({
    anime: {} as IAnimeDetails,
    setAnime: (state: IAnimeDetails) => set({ anime: state }),

    selectedEpisode: '',
    setSelectedEpisode: (state: string) => set({ selectedEpisode: state }),
}))

export const { useBoundStore: useAnimeStore } = createStoreFactory<IAnimeStore>(createAnimeStore)
