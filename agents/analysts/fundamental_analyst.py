from graph.state import ResearchState
from data.market_data import get_fundamentals
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
                {"role": "system", "content": "system_prompt_placeholder"},
                {"role": "user", "content": "user_data_placeholder"}
            ]
        }
    )
    result = response.json()["choices"][0]["message"]["content"]
    return {"fundamentals_report": result}

    
