import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const { query } = await req.json();

  // YouTube API + distilBERT integration here
  const filteredVideos = [
    { title: "Video 1", link: "https://www.youtube.com/watch?v=12345" },
    { title: "Video 2", link: "https://www.youtube.com/watch?v=67890" },
  ];

  const reply = filteredVideos.map((video) => `<a href="${video.link}" target="_blank">${video.title}</a>`).join('<br>');

  return NextResponse.json({ reply });
}