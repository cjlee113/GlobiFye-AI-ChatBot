from transformers import DistilBertTokenizer, DistilBertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the tokenizer and model in one function
def load_model():
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    model = DistilBertModel.from_pretrained("distilbert-base-uncased")
    return tokenizer, model

def get_embedding(text, tokenizer, model):
    """Generate DistilBERT embedding for a given text."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    # Pool the output to get the [CLS] token representation
    return outputs.last_hidden_state[:, 0, :].detach().numpy()

def score_similarity(query, videos, tokenizer, model, threshold=0.6):
    """
    Scores and filters videos based on similarity to the query.
    
    Parameters:
    - query: string, the search query based on resume keywords
    - videos: list of dictionaries, each containing 'title' and 'description' of a video
    - threshold: float, minimum similarity score to consider relevant

    Returns:
    - List of videos that meet the similarity threshold
    """
    query_embedding = get_embedding(query, tokenizer, model)

    relevant_videos = []
    for video in videos:
        video_text = f"{video['title']} {video['description']}"
        video_embedding = get_embedding(video_text, tokenizer, model)
        
        # Calculate cosine similarity between query and video embedding
        similarity = cosine_similarity(query_embedding, video_embedding).flatten()[0]
        
        if similarity >= threshold:
            relevant_videos.append({**video, 'similarity_score': similarity})

    # Sort videos by similarity score, highest first
    relevant_videos.sort(key=lambda x: x['similarity_score'], reverse=True)
    return relevant_videos