import { SearchAnimeParams } from "@/types/anime";

export const normalizeSearchQuery = (query: string) => query.trim();

export const normalizeSearchParams = (
  params: SearchAnimeParams,
): SearchAnimeParams => {
  const normalizedQuery = normalizeSearchQuery(
    typeof params.q === "string" ? params.q : "",
  );
  const page = params.page ?? 1;

  return {
    ...params,
    q: normalizedQuery,
    page,
  };
};
