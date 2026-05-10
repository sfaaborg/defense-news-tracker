import requests
from datetime import datetime, timedelta

API_KEY = "93ffc4b2b6f5c161dd315a71b84e2408"
BASE_URL = "https://gnews.io/api/v4/search"

def fetch_articles(query, days=25, max_results=10):
    from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    params = {
        "q": query,
        "token": API_KEY,
        "lang": "en",
        "sortby": "publishedAt",
        "from": from_date,
        "max": max_results
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if "errors" in data:
        print(f"API Error: {data['errors']}")
        return []
    articles = data.get("articles", [])
    print(f"Found {len(articles)} articles\n")
    return articles

def print_articles(articles, header):
    if not articles:
        print("No articles found.")
        return
    print(f"--- {header} ---\n")
    for i, article in enumerate(articles, 1):
        published = article["publishedAt"][:10]
        print(f"{i}. {article['title']}")
        print(f"   Published: {published}")
        print(f"   Source:    {article['source']['name']}")
        print(f"   Summary:   {article.get('description', 'N/A')}")
        print(f"   Link:      {article['url']}")
        print()

query = '"European defense spending" OR "EU defense budget" OR "NATO defense spending"'
articles = fetch_articles(query)
print_articles(articles, "European defense spending news")