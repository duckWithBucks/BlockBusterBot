import requests

# Replace with your own NewsAPI key
API_KEY = "2e0ebb19013d4e06bc4eaa5cd8d9d465"

def get_top_headlines(country="us", page_size=10):
    url = "https://newsapi.org/v2/everything?q=Apple&from=2025-09-29&sortBy=popularity&apiKey=API_KEY"
    params = {
        "country": country,   # 'my' is Malaysia
        "pageSize": page_size,
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code != 200 or data.get("status") != "ok":
        print("Error fetching news:", data.get("message", "Unknown error"))
        return []

    return data["articles"]

def display_headlines(articles):
    for i, article in enumerate(articles, start=1):
        print(f"{i}. {article['title']}")
        if article.get("source"):
            print(f"   Source: {article['source']['name']}")
        if article.get("url"):
            print(f"   Link: {article['url']}")
        print()

if __name__ == "__main__":
    headlines = get_top_headlines()
    display_headlines(headlines)
