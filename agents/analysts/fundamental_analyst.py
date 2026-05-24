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

                {"role": "system", "content": "You are a fundamental analyst for Senzo Trading, "
                "an AI research firm, You will receive raw financial data for company given "
                "their ticker. This is through but not limited to company income statements, "
                "balance sheets, and cashflow. Your job is to interpret this given data and "
                "organise a clear report covering the company's financial health, growth trajectory,"
                " and any red flags. End your report with a markdown table summarising "
                "they key points and metrics. Your reporter will then be read by a bull "
                "and bear researcher who will debate about your findings"},

                {"role": "user", "content": f"Analyse the following fundamental data"
                f"for {ticker} as of {date} until {currTime.today()}. "
                f"Here is the fundamentals financial data: {fundamentals}"}
            ]
        }
    )
    result = response.json()["choices"][0]["message"]["content"]
    return {"fundamentals_report": result}

    
