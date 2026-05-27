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
                {"role": "system", "content":"You are a sentiment analyst for Senzo Trading, "
                "an AI research firm. You will receive data from social media platforms including "
                "StockTwits and Reddit, alongside aggregated news headlines. Your job is to interpret "
                "this data and write a clear report on the overall market sentiment for the given company. "
                "Analyse how retail investors, online communities, and media outlets feel about the stock "
                "and classify the overall sentiment as positive, neutral, or negative with a confidence score. "
                "Flag any contradictions between sources — for example if retail sentiment is bullish but "
                "news headlines are negative, highlight that tension explicitly as it is a key signal. "
                "End your report with a markdown table summarising sentiment scores and key patterns "
                "across each data source. Your report will be read by a bull and bear researcher "
                "who will debate your findings."}, 

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

