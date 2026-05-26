import yfinance as yf 
import requests
from market_data import get_news


def get_reddit_sentiment(ticker):
    subreddits = ["wallstreetbets", "stocks", "investing", "stockmarket"]
    headers = {"User-Agent": "Mozilla/5.0"}
    lines = []

    for subreddit in subreddits:
        url = f"https://www.reddit.com/r/{subreddit}/search.json?q={ticker}&restrict_sr=1&sort=new"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            continue
            
        posts = response.json()["data"]["children"]
        
        for post in posts:
            data = post["data"]
            title = data["title"]
            score = data["score"]
            subreddit_name = data["subreddit"]
            lines.append(f"[r/{subreddit_name} · score:{score}] {title}")

    return "\n".join(lines)

def get_news_sentiment(ticker):
    # call ticker 
    ticker_news = get_news(ticker)
    # format the results 
    lines = []
    for news in ticker_news:
        title = news["content"]["title"]
        pub_date = news["content"]["pubDate"]
        summary = news["content"]["summary"]
        lines.append(f"[{pub_date}] {title} — {summary}")

    return "\n".join(lines)
 