import sys
import time
from pathlib import Path
# 1. Dynamically append 'senzo_trading' to the system path
current_file = Path(__file__).resolve()
for parent in current_file.parents:
    if parent.name == "senzo_trading":
        sys.path.append(str(parent))
        break
    
import yfinance as yf 
import requests
from data.market_data import get_news


def get_reddit_sentiment(ticker):
    """
    Fetches recent post titles from target subreddits using Reddit's public JSON 
    endpoints, bypassing the need for tedious official API app registration.
    """
    subreddits = ["wallstreetbets", "stocks", "investing", "stockmarket"]
    
    headers = {
        "User-Agent": f"python:senzo_trading_sentiment_fetcher:v1.0 (by /u/senzo_trading_dev)"
    }
    lines = []

    for subreddit in subreddits:
        url = f"https://www.reddit.com/r/{subreddit}/search.json?q={ticker}&restrict_sr=1&sort=new"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            # If Reddit rate-limits or blocks a specific subreddit, log it and skip to protect the loop
            if response.status_code != 200:
                print(f"[Warning] Skipping r/{subreddit} - Status code: {response.status_code}")
                continue
                
            posts = response.json().get("data", {}).get("children", [])
            
            for post in posts:
                data = post.get("data", {})
                title = data.get("title", "No Title")
                score = data.get("score", 0)
                subreddit_name = data.get("subreddit", subreddit)
                
                lines.append(f"[r/{subreddit_name} · score:{score}] {title}")
                
        except Exception as e:
            print(f"[Error] Failed to fetch r/{subreddit}: {e}")
            continue
            
        time.sleep(1)

    return "\n".join(lines)

def get_news_sentiment(ticker):
    # call ticker 
    ticker_news = get_news(ticker)
    # format the results 
    lines = []
    for news in ticker_news:
        # within content, get these fields
        title = news["content"]["title"]
        pub_date = news["content"]["pubDate"]
        summary = news["content"]["summary"]
        lines.append(f"[{pub_date}] {title} — {summary}")

    return "\n".join(lines)
 