from fastapi import FastAPI, HTTPException
from app.news_fetcher import fetch_news
from app.NER import extract_named_entities, concat_entity
from app.SA import analyze_sentiment
from app.constraints import NEWS_API_KEY


app = FastAPI()

API_KEY = NEWS_API_KEY

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial News Analysis API"}

@app.get("/analyze_news/")
def analyze_news(query: str = "stock"):
    try:
        news_data = fetch_news(API_KEY, query=query)
        results = []

        for item in news_data:
            title = item["text"]
            source = item["source"]

            # Step 1: NER
            entities = extract_named_entities(title)
            entitie = concat_entity(entities)

            # Step 2: Sentiment
            sentiment = analyze_sentiment(title)

            if(sentiment['label']!='neutral'):
                results.append({
                    "title": item['title'],
                    "desc" : item["desc"],
                    "source": source,
                    "entities": entitie,
                    "sentiment": sentiment['label']
                })

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
