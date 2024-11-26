import googleapiclient.discovery
import os

def search_youtube(query, max_results=5):
    """Searches YouTube for videos based on the given query."""
    api_key = os.getenv("AIzaSyBtfyXa2j64VaBKWao87Mjnvqi67N0VltA")
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    return response.get('items', [])