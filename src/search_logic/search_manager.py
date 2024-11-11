from video_retrieval.youtube_API import search_youtube
from video_retrieval.video_selector import select_top_videos

def perform_search(query):
    """Manages and executes search using the YouTube API and filters results."""
    results = search_youtube(query)
    return select_top_videos(results)