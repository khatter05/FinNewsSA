from transformers import pipeline
from app.constraints import SA


SA_MODEL = SA
sentiment_pipeline = pipeline("sentiment-analysis", model=SA_MODEL)

def analyze_sentiment(text):
    result = sentiment_pipeline(text)
    return result[0]  # Return the first result (label and score)
