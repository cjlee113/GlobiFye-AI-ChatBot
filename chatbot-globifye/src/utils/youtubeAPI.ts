export const fetchYouTubeVideos = async (query: string) => {
  try {
    if (!query) {
      throw new Error("Query parameter is required");
    }

    const apiKey = "AIzaSyDbovgPVGF2aCenY8LTJGvn35dIWZUHw50"; // Ensure the API key is set
    const response = await fetch(
      `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(query)}&key=${apiKey}`
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error("API Error:", errorText);
      throw new Error("Failed to fetch YouTube videos");
    }

    const data = await response.json();

    // Check if the 'items' array exists in the response
    if (!data.items || data.items.length === 0) {
      return [];
    }

    // Map the response to the necessary data fields
    const videos = data.items.map((item: any) => ({
      videoId: item.id.videoId, // Add videoId for embedding
      thumbnail: item.snippet.thumbnails.medium.url, // Get medium thumbnail
      title: item.snippet.title, // Video title
      description: item.snippet.description, // Video description
    }));

    return videos;
  } catch (error) {
    console.error("Error fetching YouTube videos:", error);
    return [];
  }
};