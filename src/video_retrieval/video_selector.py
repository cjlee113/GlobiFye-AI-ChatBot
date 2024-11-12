from transformers import DistilBertTokenizer, DistilBertModel
from youtube_API import search_youtube
from ..nlp_filtering.distilbert_filter import score_similarity, load_model

def select_videos(query):
    """Automatically selects videos based on relevance to resume keywords"""
    tokenizer, model = load_model()
    videos = search_youtube(query)
    selected_videos = []
    threshold = .95
    while len(selected_videos) < 10:
        relevant_videos = score_similarity(query, videos, tokenizer, model, threshold)
        if len(relevant_videos) >= 10:
            selected_videos.append(relevant_videos[:10])
        else:
            selected_videos.append(relevant_videos)
        threshold -= .05
    return selected_videos