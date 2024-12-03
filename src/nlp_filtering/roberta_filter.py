from transformers import RobertaConfig, RobertaModel, RobertaTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import torch
import re

# Load the tokenizer and model
def load_model():
    config = RobertaConfig()
    model = RobertaModel(config)
    tokenizer = RobertaTokenizer.from_pretrained("FacebookAI/roberta-base")
    return tokenizer, model

# Generate RoBERTa embedding for a given text
def get_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    return outputs.last_hidden_state

# Extract keywords from the query
def extract_keywords(query):
    """Extract keywords from the query, removing common stop words."""
    stop_words = {"for", "in", "and", "the", "a", "an", "on", "of", "to", "with"}
    words = re.findall(r'\w+', query.lower())
    keywords = [word for word in words if word not in stop_words]
    return keywords

# Score and filter videos based on similarity and keyword emphasis
def score_similarity(query, videos, model, keyword_weight=1.5, threshold=0.6):
    query_embedding = get_embedding(query, model)
    keywords = extract_keywords(query)
    relevant_videos = []

    for video in videos:
        # Combine title and description for text analysis
        video_text = f"{video['title']} {video['description']}"
        video_embedding = get_embedding(video_text, model)

        # Calculate cosine similarity
        similarity = cosine_similarity([query_embedding], [video_embedding]).flatten()[0]

        # Keyword Matching
        keyword_matches = sum(1 for keyword in keywords if keyword in video_text.lower())
        if 'tags' in video:
            keyword_matches += sum(1 for keyword in keywords if keyword in [tag.lower() for tag in video['tags']])
        
        keyword_score = keyword_weight * keyword_matches  # Boost score based on keyword matches

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
            0.5 * similarity +  # Weight for semantic similarity
            0.3 * keyword_score +  # Weight for keyword emphasis
            0.2 * popularity_score  # Weight for engagement metrics
        )

        # Boost less popular but useful videos
        if views < 10000 and similarity > 0.6:
            relevance_score += 0.1  # Boost score for less popular but relevant videos

        # Add video to results if relevance score meets the threshold
        if relevance_score >= threshold:
            relevant_videos.append({**video, 'similarity_score': relevance_score})

    # Sort videos by relevance score, highest first
    relevant_videos.sort(key=lambda x: x['similarity_score'], reverse=True)
    return relevant_videos

# Example usage:
model = load_model()