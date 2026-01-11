import { SEARCH_ANIME } from "@/constants/query-keys";
import { api } from "@/lib/api";
import { IAnimeSearch, SearchAnimeParams } from "@/types/anime";
import { useQuery } from "react-query";
import { PLACEHOLDER_POSTER } from "@/utils/constants";

type BackendAnime = {
  id: string;
  title: string;
  title_original?: string | null;
  status?: string | null;
  year?: number | null;
};

const searchAnime = async (params: SearchAnimeParams) => {
  const limit = 20;
  const currentPage = params.page || 1;
  const offset = (currentPage - 1) * limit;
  const emptyResult: IAnimeSearch = {
    animes: [],
    totalPages: currentPage,
    hasNextPage: false,
    currentPage,
  };

  try {
    const res = await api.get<BackendAnime[]>("/search/anime", {
      params: { q: params.q, limit, offset },
    });

    const animes = (res.data || []).map((anime) => ({
      id: anime.id,
      name: anime.title,
      jname: anime.title_original || anime.title,
      poster: PLACEHOLDER_POSTER,
      episodes: { sub: null, dub: null },
      type: anime.status || undefined,
      rank: undefined,
    }));

    const hasNextPage = animes.length === limit;
    const estimatedTotal =
      animes.length === 0 || animes.length < limit
        ? currentPage
        : currentPage + 1;

    return {
      animes,
      totalPages: estimatedTotal,
      hasNextPage,
      currentPage,
    };
  } catch (error) {
    console.error("Search anime failed", error);
    return emptyResult;
  }
};

export const useGetSearchAnimeResults = (params: SearchAnimeParams) => {
  return useQuery({
    queryFn: () => searchAnime(params),
    queryKey: [SEARCH_ANIME, { ...params }],
    enabled: (params.q || "").trim().length >= 2,
    retry: false,
  });
};
