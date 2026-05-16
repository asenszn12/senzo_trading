import yfinance as yf 

ticker = yf.Ticker('AAPL') ## find way for ppl to type in ticker
print(ticker.info) ## all info about the company
