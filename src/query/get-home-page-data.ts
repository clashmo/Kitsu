import { GET_HOME_PAGE_DATA } from "@/constants/query-keys";
import { api } from "@/lib/api";
import { IAnimeData } from "@/types/anime";
import { useQuery } from "react-query";
import { PLACEHOLDER_POSTER } from "@/utils/constants";

type BackendAnime = {
  id: string;
  title: string;
  title_original?: string | null;
  status?: string | null;
  year?: number | null;
};

const mapAnimeList = (animes: BackendAnime[]) =>
  animes.map((anime) => ({
    id: anime.id,
    name: anime.title,
    jname: anime.title_original || anime.title,
    poster: PLACEHOLDER_POSTER,
    episodes: { sub: null, dub: null },
    type: anime.status ?? "",
    rank: undefined,
    duration: "",
    rating: null,
  }));

const getHomePageData = async () => {
  const res = await api.get<BackendAnime[]>("/anime", {
    params: { limit: 20, offset: 0 },
  });
  const mapped = mapAnimeList(res.data || []);
  const spotlightAnimes = mapped.slice(0, 5).map((anime, idx) => ({
    rank: idx + 1,
    id: anime.id,
    name: anime.name,
    description: "",
    poster: anime.poster,
    jname: anime.jname,
    episodes: anime.episodes,
    type: anime.type,
    otherInfo: [],
  }));

  // Backend currently exposes a single anime list; reuse it across sections until dedicated endpoints exist
  return {
    spotlightAnimes,
    trendingAnimes: mapped,
    latestEpisodeAnimes: mapped,
    topUpcomingAnimes: mapped,
    top10Animes: {
      today: mapped.slice(0, 10),
      week: mapped.slice(0, 10),
      month: mapped.slice(0, 10),
    },
    topAiringAnimes: mapped,
    mostPopularAnimes: mapped,
    mostFavoriteAnimes: mapped,
    latestCompletedAnimes: mapped,
    genres: [],
  } as IAnimeData;
};

export const useGetHomePageData = () => {
    return useQuery({
        queryFn: getHomePageData,
        queryKey: [GET_HOME_PAGE_DATA],
        refetchOnWindowFocus: false,
        staleTime: 1000 * 60 * 5, // 5 minutes
        cacheTime: 1000 * 60 * 10, // 10 minutes
    });
};
