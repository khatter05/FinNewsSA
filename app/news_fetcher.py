from newsdataapi import NewsDataApiClient

def fetch_news(api_key, query="stock", country="in", category="business", language="en"):
    api = NewsDataApiClient(apikey=api_key)
    response = api.news_api(q=query, country=country, category=category, language=language)
    news_data = [
        {   
            'title': result['title'],
            'desc': result['description'],
            'text': result['title'] + " " + (result['description'] or ""),
            'source': result['source_name']
        }
        for result in response.get('results', [])
    ]
    return news_data
