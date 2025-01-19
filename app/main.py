from fastapi import FastAPI, HTTPException
from app.news_fetcher import fetch_news
from app.NER import extract_named_entities, concat_entity
from app.SA import analyze_sentiment
from API import NEWS_API_KEY

app = FastAPI()
API_KEY = NEWS_API_KEY

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial News Analysis API"}

@app.get("/analyze_news/")
def analyze_news(query: str = "stock", page: str = None):
    try:
        # Fetch news data with pagination
        response = fetch_news(API_KEY, query=query, page=page)
        news_data = response["news"]
        next_page = response["next_page"]

        results = []
        for item in news_data:
            title = item["text"]
            source = item["source"]

            # Step 1: NER
            entities = extract_named_entities(title)
            entitie = concat_entity(entities)

            # Step 2: Sentiment
            sentiment = analyze_sentiment(title)

            if sentiment["label"] != "neutral":
                results.append({
                    "title": item["title"],
                    "desc": item["desc"],
                    "source": source,
                    "entities": entitie,
                    "sentiment": sentiment["label"],
                    "link" : item["link"],
                    "publish_date" : item["Date"]
                })

        return {"results": results, "next_page": next_page}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
