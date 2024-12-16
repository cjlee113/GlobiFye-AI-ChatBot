import { NextApiRequest, NextApiResponse } from "next";
import axios from "axios";

type VideoItem = {
  title: string;
  thumbnail: string;
  videoUrl: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { query } = req.query; // Read the query parameter from the request
  const API_KEY = process.env.YOUTUBE_API_KEY; // API Key from .env file
  const url = "https://www.googleapis.com/youtube/v3/search";

  if (!query) {
    return res.status(400).json({ error: "Query parameter is required" });
  }

  try {
    const response = await axios.get(url, {
      params: {
        part: "snippet",
        q: query,
        key: API_KEY,
        maxResults: 5,
      },
    });

    // Map over the response data items and create a new array with required fields
    const videos: VideoItem[] = response.data.items.map((item: any) => ({
      title: item.snippet.title,
      thumbnail: item.snippet.thumbnails.default.url,
      videoUrl: `https://www.youtube.com/watch?v=${item.id.videoId}`,
    }));

    return res.status(200).json(videos);
  } catch (error: any) {
    console.error("Error fetching YouTube videos:", error.response?.data || error.message);
    return res.status(500).json({
      error: "Failed to fetch YouTube videos",
      details: error.response?.data || "No additional details",
    });
  }
}
