import yfinance as yf 
from datetime import date


def get_fundamentals(ticker): 
    stock = yf.Ticker(ticker)
    company_info = stock.info
    company_financials = stock.financials
    company__balance_sheet = stock.balance_sheet
    company_cashflow = stock.cashflow
    return {
        "info": company_info,
        "financials": company_financials,
        "balance_sheet": company__balance_sheet,
        "cashflow": company_cashflow
    }

def price_history(ticker, start_date): 
    stock = yf.Ticker(ticker)
    company_history = stock.history(start=start_date, end=date.today())
    return company_history

def get_news(ticker):
    stock = yf.Ticker(ticker)
    company_news = stock.news
    return company_news