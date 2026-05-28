import sys
from pathlib import Path
from datetime import date as currTime
import requests
import os 
from dotenv import load_dotenv

# 1. Dynamically append 'senzo_trading' to the system path
current_file = Path(__file__).resolve()
for parent in current_file.parents:
    if parent.name == "senzo_trading":
        sys.path.append(str(parent))
        break
    
from graph.state import ResearchState
from data.sentiment_data import get_reddit_sentiment, get_news_sentiment

load_dotenv()

def sentimental_analyst_node(state: ResearchState):
    ticker = state["ticker"]
    date = state["date"]
    
    # Fetch the raw data
    reddit_sentiment_data = get_reddit_sentiment(ticker)
    news_sentiment_data = get_news_sentiment(ticker)
        
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}", 
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/auto", 
            "messages": [
                {
                    "role": "system", 
                    "content": (
                        "You are a quantitative sentiment analyst at Senzo Trading. Your job is to SYNTHESIZE data, not list it. "
                        "Do not quote individual posts or headlines. Extract the underlying market psychology and narratives. "
                        "Keep your entire response strictly to brief, hard-hitting bullet points. "
                        "\n\nFORMAT YOUR OUTPUT EXACTLY LIKE THIS:\n"
                        "### 1. Retail Sentiment (Reddit) | [Bullish/Neutral/Bearish] (XX% Confidence)\n"
                        "- [Bullet point on main retail narrative]\n"
                        "- [Bullet point on retail fears/hopes]\n"
                        "### 2. Media Sentiment (News) | [Bullish/Neutral/Bearish] (XX% Confidence)\n"
                        "- [Bullet point on main media focus]\n"
                        "- [Bullet point on macroeconomic or fundamental drivers mentioned]\n"
                        "### 3. The Contradiction (Alpha Generation)\n"
                        "- [1-2 bullet points explicitly highlighting where retail and media disagree]\n"
                        "### 4. Key Catalysts\n"
                        "- [Bullet points on recurring themes driving the stock]\n\n"
                        "End with a markdown table summarizing the scores."
                    )
                }, 
                {
                    "role": "user", 
                    "content": (
                        f"Synthesize the sentiment for {ticker} from {date} to {currTime.today()}.\n\n"
                        f"REDDIT NOISE (Extract signal only):\n{reddit_sentiment_data}\n\n"
                        f"MEDIA NOISE (Extract signal only):\n{news_sentiment_data}"
                    )
                }
            ]
        }
    )

    # Extract the LLM's response
    result = response.json()["choices"][0]["message"]["content"]
    
    return {"sentimental_report": result}

# Run the file (__name__) as main and get the test output
if __name__ == "__main__": 
    test_state = {
        "ticker": "AAPL", 
        "date": "2026-01-01"
    }
    
    # Execute the node and print the structured report
    result = sentimental_analyst_node(test_state)
    print("\n--- FINAL SENTIMENT REPORT ---\n")
    print(result["sentimental_report"])