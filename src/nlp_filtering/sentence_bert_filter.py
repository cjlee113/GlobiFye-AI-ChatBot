from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the Sentence-BERT model
def load_model():
    model = SentenceTransformer("all-MiniLM-L6-v2")  # A lightweight S-BERT model
    return model

def get_embedding(text, model):
    """Generate Sentence-BERT embedding for a given text."""
    return model.encode(text, convert_to_numpy=True)

def score_similarity(query, videos, model, threshold=0.6):
    """
    Scores and filters videos based on similarity to the query,
    and incorporates filtering by tags and engagement metrics.
    
    Parameters:
    - query: string, the search query based on resume keywords
    - videos: list of dictionaries, each containing 'title', 'description',
              'tags', 'category', 'views', 'likes', and 'dislikes'
    - threshold: float, minimum similarity score to consider relevant

    Returns:
    - List of videos that meet the similarity threshold, sorted by relevance
    """
    query_embedding = get_embedding(query, model)
    relevant_videos = []

    for video in videos:
        # Combine title and description for text analysis
        video_text = f"{video['title']} {video['description']}"
        video_embedding = get_embedding(video_text, model)

        # Calculate cosine similarity
        similarity = cosine_similarity([query_embedding], [video_embedding]).flatten()[0]

        # Tag Matching
        tag_score = 0
        if 'tags' in video:
            matching_tags = [tag for tag in video['tags'] if tag.lower() in query.lower()]
            tag_score = len(matching_tags) / (len(video['tags']) + 1e-5)  # Normalized score

        # Category Filtering
        is_relevant_category = video.get('category', '').lower() in ['education', 'science & technology']
        category_score = 1.0 if is_relevant_category else 0.5  # Penalize unrelated categories

        # Engagement Metrics
        views = video.get('views', 0)
        likes = video.get('likes', 0)
        dislikes = video.get('dislikes', 0)
        like_ratio = likes / (likes + dislikes + 1e-5)  # Handle division by zero

        # Popularity Score
        popularity_score = (views / 1e6) + like_ratio  # Weighted score
        popularity_score = min(popularity_score, 1.0)  # Cap the score at 1.0

        # Combine Scores
        relevance_score = (
            0.4 * similarity +
            0.2 * tag_score +
            0.1 * category_score +
            0.3 * popularity_score
        )

        # Penalize high popularity if not relevant
        if popularity_score > 0.8 and similarity < 0.5:
            relevance_score *= 0.7  # Reduce score if popular but not very relevant

        # Boost less popular but useful videos
        if views < 10000 and similarity > 0.6:
            relevance_score += 0.1  # Boost score for less popular but relevant videos

        # Add video to results if relevance score meets the threshold
        if relevance_score >= threshold:
            relevant_videos.append({**video, 'similarity_score': relevance_score})

    # Sort videos by relevance score, highest first
    relevant_videos.sort(key=lambda x: x['similarity_score'], reverse=True)
    return relevant_videos
