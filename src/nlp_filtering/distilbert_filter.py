from transformers import DistilBertTokenizer, DistilBertModel
import re
import requests

# Load the tokenizer and model
def load_model():
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    model = DistilBertModel.from_pretrained("distilbert-base-uncased")
    return tokenizer, model

# Extract keywords from the query
def extract_keywords(query):
    """Extract keywords from the query, removing common stop words."""
    stop_words = {"for", "in", "and", "the", "a", "an", "on", "of", "to", "with"}
    words = re.findall(r'\w+', query.lower())
    keywords = [word for word in words if word not in stop_words]
    return keywords

# Fetch videos from YouTube using the API
def fetch_youtube_videos(api_key, query, max_results=10):
    """
    Fetch videos using YouTube's search.list API.
    Filters for medium-length videos sorted by view count.
    """
    base_url = "https://www.googleapis.com/youtube/v3/search"
    keywords = "+".join(query)  # Convert keywords list into a query string
    params = {
        "part": "snippet",
        "q": keywords,
        "type": "video",
        "videoDuration": "medium",  # Medium-length videos (4-20 minutes)
        "order": "viewCount",  # Sort by popularity
        "maxResults": max_results,  # Limit results to 10
        "key": api_key,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

# Process video results
def process_videos(videos, keywords):
    """
    Process video results to filter or score them further if needed.
    Currently, this function just enriches videos with keyword match counts.
    """
    processed_videos = []
    for video in videos:
        # Combine title and description for keyword matching
        title = video['snippet']['title']
        description = video['snippet']['description']
        video_text = f"{title} {description}".lower()

        # Count keyword matches
        keyword_matches = sum(1 for keyword in keywords if keyword in video_text)

        processed_videos.append({
            "title": title,
            "description": description,
            "channel_title": video['snippet']['channelTitle'],
            "video_id": video['id']['videoId'],
            "keyword_matches": keyword_matches,
        })

    # Optionally, sort by keyword matches or other criteria
    processed_videos.sort(key=lambda x: x['keyword_matches'], reverse=True)
    return processed_videos

# Main function to integrate all steps
def search_and_filter_videos(api_key, user_query, max_results=10):
    # Load the NLP model (for future use, if needed)
    tokenizer, model = load_model()

    # Step 1: Extract keywords from user query
    keywords = extract_keywords(user_query)

    # Step 2: Use YouTube API to fetch videos
    videos = fetch_youtube_videos(api_key, keywords, max_results)

    # Step 3: Process and optionally filter videos
    filtered_videos = process_videos(videos, keywords)

    # Return the top results
    return filtered_videos

# Example usage
if __name__ == "__main__":
    API_KEY = "YOUR_YOUTUBE_API_KEY"
    query = "learn python programming for beginners"
    results = search_and_filter_videos(API_KEY, query)
    for idx, video in enumerate(results):
        print(f"{idx + 1}. {video['title']} (Keyword Matches: {video['keyword_matches']})")
        print(f"   Description: {video['description']}")
        print(f"   Channel: {video['channel_title']}")
        print(f"   Watch: https://www.youtube.com/watch?v={video['video_id']}\n")