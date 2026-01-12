import { GET_HOME_PAGE_DATA } from "@/constants/query-keys";
import { api } from "@/lib/api";
import { IAnimeData, SpotlightAnime, Type } from "@/types/anime";
import { QueryFunction, UseQueryOptions, useQuery } from "react-query";
import { PLACEHOLDER_POSTER } from "@/utils/constants";

type BackendAnime = {
  id: string;
  title: string;
  title_original?: string | null;
  status?: string | null;
  year?: number | null;
};

const mapStatusToType = (status?: string | null): Type => {
  const normalizedStatus = status?.toUpperCase();

  switch (normalizedStatus) {
    case "TV":
      return Type.Tv;
    case "ONA":
      return Type.Ona;
    case "MOVIE":
      return Type.Movie;
    default:
      return Type.Tv;
  }
};

const mapAnimeList = (animes: BackendAnime[]) =>
  animes.map((anime) => ({
    id: anime.id,
    name: anime.title,
    jname: anime.title_original || anime.title,
    poster: PLACEHOLDER_POSTER,
    episodes: { sub: null, dub: null },
    type: mapStatusToType(anime.status),
    rank: undefined,
    duration: "",
    rating: null,
  }));

const getHomePageData: QueryFunction<IAnimeData, [string]> = async () => {
  const emptyData: IAnimeData = {
    spotlightAnimes: [],
    trendingAnimes: [],
    latestEpisodeAnimes: [],
    topUpcomingAnimes: [],
    top10Animes: {
      today: [],
      week: [],
      month: [],
    },
    topAiringAnimes: [],
    mostPopularAnimes: [],
    mostFavoriteAnimes: [],
    latestCompletedAnimes: [],
    genres: [],
  };

  try {
    const res = await api.get<BackendAnime[]>("/anime", {
      params: { limit: 20, offset: 0 },
    });
    const mapped = mapAnimeList(res.data || []);
    const spotlightAnimes: SpotlightAnime[] = mapped.slice(0, 5).map((anime, idx) => ({
      rank: idx + 1,
      id: anime.id,
      name: anime.name,
      description: "",
      poster: anime.poster,
      jname: anime.jname,
      episodes: anime.episodes,
      type: anime.type ?? Type.Tv,
      otherInfo: [],
    }));

    const data: IAnimeData = {
      ...emptyData,
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
    };

    return data;
  } catch (error) {
    console.error("Failed to load home page data", error);
    return emptyData;
  }
};

export const useGetHomePageData = (
  options?: UseQueryOptions<IAnimeData, Error, IAnimeData, [string]>,
) => {
  return useQuery<IAnimeData, Error, IAnimeData, [string]>({
    queryFn: getHomePageData,
    queryKey: [GET_HOME_PAGE_DATA],
    refetchOnWindowFocus: false,
    staleTime: 1000 * 60 * 5, // 5 minutes
    cacheTime: 1000 * 60 * 10, // 10 minutes
    retry: false,
    ...options,
  });
};
