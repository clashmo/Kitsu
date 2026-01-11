import { SEARCH_ANIME } from "@/constants/query-keys";
import { api } from "@/lib/api";
import { ISuggestionAnime } from "@/types/anime";
import { useQuery } from "react-query";
import { PLACEHOLDER_POSTER } from "@/utils/constants";

const searchAnime = async (q: string) => {
  if (q === "") {
    return;
  }
  const res = await api.get("/search/anime", {
    params: {
      q,
      limit: 5,
      offset: 0,
    },
  });

  return (res.data || []).map((anime: any) => ({
    id: anime.id,
    name: anime.title,
    jname: anime.title_original || anime.title,
    poster: PLACEHOLDER_POSTER,
    episodes: { sub: null, dub: null },
    type: anime.status || undefined,
    rank: undefined,
    moreInfo: [],
  })) as ISuggestionAnime[];
};

export const useSearchAnime = (query: string) => {
  return useQuery({
    queryFn: () => searchAnime(query),
    queryKey: [SEARCH_ANIME, query],
    enabled: query.trim().length >= 2,
  });
};
