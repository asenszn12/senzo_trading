import sys
import time
import random
import requests
import xml.etree.ElementTree as ET
from pathlib import Path

# 1. Dynamically append 'senzo_trading' to the system path
current_file = Path(__file__).resolve()
for parent in current_file.parents:
    if parent.name == "senzo_trading":
        sys.path.append(str(parent))
        break
    
from data.market_data import get_news


def get_random_header():
    """
    Generates a randomized browser profile header to fragment the scraper's footprint
    and avoid presenting a static signature to firewalls.
    """
    user_agents = [
        # Chrome on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        # Safari on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
        # Edge on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        # Chrome on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ]
    
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0"
    }


def get_reddit_sentiment(ticker):
    """
    Bypasses Reddit's strict JSON WAF blocks by querying the public RSS search feeds instead.
    Uses precise boolean keyword constraints and temporal filters to isolate high-signal posts.
    """
    subreddits = ["wallstreetbets", "stocks", "investing"]
    lines = []

    # Format strict query: forces exact ticker match or title match to reduce false positives
    query = f'title:"{ticker}" OR "{ticker}"'

    for subreddit in subreddits:
        # &t=week limits results strictly to the last 7 days
        url = f"https://www.reddit.com/r/{subreddit}/search.rss?q={query}&restrict_sr=1&sort=new&t=week"
        
        try:
            # Generate a unique browser mask for this specific request loop
            headers = get_random_header()
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code in [403, 429]:
                lines.append(f"<r/{subreddit} unavailable: Reddit firewall blocked the RSS request ({response.status_code})>")
                continue
            elif response.status_code != 200:
                lines.append(f"<r/{subreddit} unavailable: Status {response.status_code}>")
                continue
                
            # Parse the Atom XML feed safely
            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('atom:entry', ns)
            
            if not entries:
                lines.append(f"<r/{subreddit}: No recent posts found for {ticker} within the last week>")
                continue
                
            for entry in entries[:5]:  # Extract the top 5 most recent relevant posts
                title_node = entry.find('atom:title', ns)
                if title_node is not None and title_node.text:
                    lines.append(f"[r/{subreddit}] {title_node.text.strip()}")
                
        except ET.ParseError:
            lines.append(f"<r/{subreddit} unavailable: Failed to parse Reddit RSS XML>")
        except Exception as e:
            lines.append(f"<r/{subreddit} unavailable: Exception - {str(e)}>")
            
        # Polite throttling gap between subreddit queries
        time.sleep(1.5)

    return "\n".join(lines) if lines else "<unavailable: all Reddit fetches failed>"


def get_news_sentiment(ticker):
    """
    Retrieves and returns the pre-formatted news string directly from market_data.py
    """
    try:
        news = get_news(ticker)
        return news if news else "<unavailable: No news found>"
    except Exception as e:
        return f"<unavailable: Error fetching news - {str(e)}>"