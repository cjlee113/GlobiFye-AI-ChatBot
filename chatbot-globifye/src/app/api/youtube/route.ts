import { NextApiRequest } from 'next';
import axios from 'axios';
import { NextResponse } from 'next/server';  // Import NextResponse

type VideoItem = {
  title: string;
  thumbnail: string;
  videoUrl: string;
};

export async function GET(req: NextApiRequest) {
  const { query } = req.nextUrl.searchParams;  // Use nextUrl for query params
  const API_KEY = process.env.YOUTUBE_API_KEY;  // API key from .env.local
  const url = 'https://www.googleapis.com/youtube/v3/search';

  if (!query) {
    // Return a response using NextResponse
    return NextResponse.json({ error: 'Query parameter is required' }, { status: 400 });
  }

  try {
    const response = await axios.get(url, {
      params: {
        part: 'snippet',
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

    // Return videos using NextResponse
    return NextResponse.json(videos, { status: 200 });
  } catch (error) {
    console.error('Error fetching YouTube videos:', error);
    return NextResponse.json({ error: 'Failed to fetch YouTube videos' }, { status: 500 });
  }
}