import { GET_ANIME_DETAILS } from "@/constants/query-keys";
import { api } from "@/lib/api";
import { IAnimeDetails } from "@/types/anime-details";
import { useQuery } from "react-query";
import { PLACEHOLDER_POSTER } from "@/utils/constants";

type BackendAnime = {
  id: string;
  title: string;
  title_original?: string | null;
  description?: string | null;
  year?: number | null;
  status?: string | null;
};

type BackendRelease = {
  id: string;
  anime_id: string;
  title: string;
  year?: number | null;
  status?: string | null;
};

const getAnimeDetails = async (animeId: string) => {
  const [animeRes, releasesRes] = await Promise.all([
    api.get<BackendAnime>(`/anime/${animeId}`),
    api.get<BackendRelease[]>("/releases", { params: { limit: 100, offset: 0 } }),
  ]);

  const anime = animeRes.data;
  const releases =
    (releasesRes.data || []).filter((release) => release.anime_id === animeId) ||
    [];

  const seasons = releases.map((release, idx) => ({
    id: release.id,
    name: release.title,
    title: release.title,
    poster: PLACEHOLDER_POSTER,
    isCurrent: idx === 0,
  }));

  const mapped: IAnimeDetails = {
    anime: {
      info: {
        id: anime.id,
        anilistId: 0,
        malId: 0,
        name: anime.title,
        poster: PLACEHOLDER_POSTER,
        description: anime.description || "",
        stats: {
          rating: anime.status || "",
          quality: "",
          episodes: { sub: 0, dub: 0 },
          type: anime.status || "Unknown",
          duration: "",
        },
        promotionalVideos: [],
        charactersVoiceActors: [],
      },
      moreInfo: {
        japanese: anime.title_original || anime.title,
        synonyms: "",
        aired: anime.year ? anime.year.toString() : "N/A",
        premiered: "",
        duration: "",
        status: anime.status || "Unknown",
        malscore: "",
        genres: [],
        studios: "",
        producers: [],
      },
    },
    seasons,
    mostPopularAnimes: [],
    relatedAnimes: [],
    recommendedAnimes: [],
  };

  return mapped;
};

export const useGetAnimeDetails = (animeId: string) => {
  return useQuery({
    queryFn: () => getAnimeDetails(animeId),
    queryKey: [GET_ANIME_DETAILS, animeId],
  });
};
