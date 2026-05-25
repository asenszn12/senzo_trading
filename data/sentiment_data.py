import yfinance as yf 
import os 
import requests

def get_stocktwits_sentiment(ticker, date):
    response = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json")
    # get the date from this point of time given 
    data = response.json()
    messages = data["messages"] 

    lines = []
    bullish = 0
    bearish = 0
    unlabeled = 0

    for message in messages: 
        body = message["body"]
        created = message["created_at"]
        sentimental_obj = message["entities"]["sentiment"]

        if sentimental_obj and sentimental_obj["basic"] == "Bullish":
            bullish += 1 
            tag = "Bullish"

        elif sentimental_obj and sentimental_obj["basic"] == "Bearish":
            bearish += 1 
            tag = "Bearish"

        else:
            unlabeled += 1
            tag = "Unlabeled"

        lines.append(f"[{created} · {tag}] {body}")
        
    total = bullish + bearish + unlabeled
    summary = f"Bullish: {bullish} · Bearish: {bearish} · Unlabeled: {unlabeled} · Total: {total}"
    return summary + "\n\n" + "\n".join(lines)

def get_reddit_sentiment(ticker, date):

    pass 
def get_news_sentiment(ticker, date):

    pass