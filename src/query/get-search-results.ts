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

  return {
    animes,
    totalPages: animes.length ? currentPage + 1 : currentPage,
    hasNextPage: animes.length === limit,
    currentPage,
  } as IAnimeSearch;
};

export const useGetSearchAnimeResults = (params: SearchAnimeParams) => {
  return useQuery({
    queryFn: () => searchAnime(params),
    queryKey: [SEARCH_ANIME, { ...params }],
    enabled: (params.q || "").trim().length >= 2,
  });
};
