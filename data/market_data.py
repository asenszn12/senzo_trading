import yfinance as yf 

ticker = yf.Ticker('AAPL') ## find way for ppl to type in ticker
print(ticker.news) ## all info about the company

# get as much info as you can from the yfinance 
# can use to get fundamentals data and technical too 
def get_fundamentals(ticker, date): 
    pass

def price_history(ticker, date): 
    pass 

def get_news(ticker):
    pass