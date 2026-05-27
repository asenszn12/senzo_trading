import sys
sys.path.append('/Users/aadhi/senzo_trading')
from graph.state import ResearchState
from data.market_data import get_fundamentals
from datetime import date as currTime
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

def fundamental_analyst_node(state: ResearchState):
    ticker = state["ticker"]
    date = state["date"]

    fundamentals = get_fundamentals(ticker)
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }, 
        json={
            "model": "openrouter/free",
            "messages": [
                {"role": "system", "content": "You are a fundamental analyst at Senzo Trading, "
                "an AI research firm. You will receive raw financial data for a company including "
                "income statements, balance sheets, and cashflow statements. Interpret this data "
                "and write a concise research report covering financial health, growth trajectory, "
                "and any red flags. End with a markdown table of key metrics. Your report will "
                "be read by a bull and bear researcher who will debate your findings."},

                {"role": "user", "content": f"Analyse the following fundamental data "
                f"for {ticker} as of {date} until {currTime.today()}. "
                f"Here is the fundamentals financial data: {fundamentals}"}
            ]
        }
    )
    result = response.json()["choices"][0]["message"]["content"]
    return {"fundamentals_report": result}

if __name__ == "__main__":
    test_state = {
        "ticker": "AAPL",
        "date": "2026-01-01"
    }
    result = fundamental_analyst_node(test_state)
    print(result)