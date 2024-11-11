import os
from utils.config_loader import load_config
from utils.logger import setup_logger
from data_processing.resume_processor import process_resume
from video_retrieval.youtube_API import get_youtube_videos
from nlp_filtering.distilbert_filter import load_model, score_similarity

# Load configuration and setup logger
config = load_config("config.yaml")
logger = setup_logger()

def main():
    try:
        # Load the DistilBERT model
        tokenizer, model = load_model()

        # Sample input: Processed resume data
        resume_text = "Experienced software engineer skilled in Python, Java, data structures, algorithms, and machine learning."
        
        # Step 1: Extract keywords from the resume text
        keywords = process_resume(resume_text)
        logger.info(f"Extracted Keywords: {keywords}")

        # Step 2: Retrieve videos from YouTube using the extracted keywords
        videos = get_youtube_videos(keywords, config["youtube_api_key"])
        logger.info(f"Retrieved {len(videos)} videos from YouTube.")

        # Step 3: Filter videos using DistilBERT for relevance
        relevant_videos = score_similarity(" ".join(keywords), videos, tokenizer, model, threshold=0.5)
        logger.info(f"Filtered down to {len(relevant_videos)} relevant videos.")

        # Step 4: Display the relevant videos
        print("Relevant Videos:")
        for video in relevant_videos:
            print(f"Title: {video['title']}")
            print(f"Description: {video['description']}")
            print(f"Similarity Score: {video['similarity_score']:.2f}")
            print("-" * 40)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()