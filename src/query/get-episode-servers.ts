import { GET_EPISODE_SERVERS } from "@/constants/query-keys";
import axios from "axios";
import { IEpisodeServers } from "@/types/episodes";
import { useQuery } from "react-query";

const getEpisodeServers = async (episodeId: string) => {
  const res = await axios.get("/api/episode/servers", {
    params: {
      animeEpisodeId: decodeURIComponent(episodeId),
    },
  });
  return res.data.data as IEpisodeServers;
};

export const useGetEpisodeServers = (episodeId: string) => {
  return useQuery({
    queryFn: () => getEpisodeServers(episodeId),
    queryKey: [GET_EPISODE_SERVERS, episodeId],
    refetchOnWindowFocus: false,
  });
};
