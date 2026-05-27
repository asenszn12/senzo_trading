import sys
sys.path.append('/Users/aadhi/senzo_trading')
from graph.state import ResearchState
import requests
import os 
from dotenv import load_dotenv
from data.sentiment_data import get_reddit_sentiment, get_news_sentiment


load_dotenv()

def sentimental_analyst_node(state: ResearchState):
    ticker = state["ticker"]
    date = state["date"]
    reddit_sentiment_data = get_reddit_sentiment(ticker)
    news_sentiment_data = get_news_sentiment(ticker)

    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}", 
            "Content-Type":"application/json"
        } ,
        json={
            "model": "openrouter/free", 
            "messages": [
                {"role": "system", "content":"You are a sentiment analyst at Senzo Trading. You will receive Reddit posts from r/wallstreetbets, r/stocks, r/investing, and r/stockmarket alongside news headlines. "
                "Interpret this data and write a structured sentiment report covering: "
                "(1) overall retail sentiment from Reddit scored bullish/neutral/bearish with confidence percentage, "
                "(2) overall media sentiment from news headlines scored the same way, "
                "(3) any contradictions between retail and media sentiment flagged explicitly, "
                "(4) key recurring themes across both sources. "
                "End with a markdown table summarising sentiment scores per source. "
                "Your report will be read by a bull and bear researcher who will debate your findings."}, 

                {"role": "user", "content":f"Analyse sentiment for {ticker} as of {date}.\n\n"
                f"REDDIT:\n{reddit_sentiment_data}\n\n"
                f"NEWS:\n{news_sentiment_data}"}
            ]
        } )


    result = response.json()["choices"][0]["message"]["content"]
    return {"sentimental_report": result}

# run the file (__name__) as main and get the test output
if __name__ == "__main__": 

    test_state = {
        "ticker": "AAPL", 
        "date": "2026-01-01"
    }
    result = sentimental_analyst_node(test_state)
    print(result)

