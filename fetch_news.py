import requests
import json
from datetime import datetime, timedelta

import os
API_KEY = os.environ.get("GNEWS_API_KEY", "93ffc4b2b6f5c161dd315a71b84e2408")
BASE_URL = "https://gnews.io/api/v4/search"

TOPICS = [
    {
        "title": "European Defense Spending",
        "query": '"European defense spending" OR "EU defense budget" OR "NATO defense spending"'
    },
    {
        "title": "National Defense Strategies",
        "query": '"national defense strategy" OR "national security strategy" OR "defence white paper"'
    },
    {
        "title": "Global Military News",
        "query": '"military strategy" OR "defense policy" OR "armed forces"'
    }
]

def fetch_articles(query, days=25, max_results=5):
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
    return data.get("articles", [])

output = {
    "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "topics": []
}

for topic in TOPICS:
    print(f"Fetching: {topic['title']}...")
    articles = fetch_articles(topic["query"])
    output["topics"].append({
        "title": topic["title"],
        "articles": articles
    })
    print(f"  Found {len(articles)} articles")

with open("news.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nDone! Saved to news.json")