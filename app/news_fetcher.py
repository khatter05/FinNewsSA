from newsdataapi import NewsDataApiClient

def fetch_news(api_key, query="stock", country="in", category="business", language="en", page=None):
    """
    Fetch news articles with pagination support.

    :param api_key: API key for NewsDataApiClient
    :param query: Search query
    :param country: Country filter
    :param category: News category filter
    :param language: Language filter
    :param page: Page number for pagination
    :return: Dictionary containing news data and next page token
    """
    api = NewsDataApiClient(apikey=api_key)
    response = api.news_api(
        q=query,
        country=country,
        category=category,
        language=language,
        page=page,
        timezone = "Asia/Kolkata",
        removeduplicate = True
    )

    # Extract news data
    news_data = [
        {
            'title': result.get('title', 'No Title'),
            'desc': result.get('description', 'No Description'),
            'text': result.get('title', '') + " " + (result.get('description', '') or ""),
            'source': result.get('source_name', 'Unknown Source'),
            'link' : result.get('link','no URL'),
            'Date' : result.get('pubDate','no publish date')
        }
        for result in response.get('results', [])
    ]

    # Get next page token
    next_page = response.get('nextPage', None)

    return {"news": news_data, "next_page": next_page}
