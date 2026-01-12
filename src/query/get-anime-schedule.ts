import { GET_ANIME_SCHEDULE } from "@/constants/query-keys";
import axios from "axios";
import { IAnimeSchedule } from "@/types/anime-schedule";
import { useQuery } from "react-query";

const getAnimeSchedule = async (date: string) => {
  const queryParams = date ? `?date=${date}` : "";

  try {
    const res = await axios.get("/api/schedule" + queryParams, { timeout: 10000 });
    return res.data.data as IAnimeSchedule;
  } catch (error) {
    console.error("Failed to fetch schedule", error);
    return { scheduledAnimes: [] } as IAnimeSchedule;
  }
};

export const useGetAnimeSchedule = (
  date: string,
  options?: { enabled?: boolean },
) => {
  return useQuery({
    queryFn: () => getAnimeSchedule(date),
    queryKey: [GET_ANIME_SCHEDULE, date],
    retry: false,
    enabled: options?.enabled ?? true,
  });
};
