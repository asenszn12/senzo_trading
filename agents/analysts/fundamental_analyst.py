from graph.state import ResearchState
from openrouter import OpenRouter 
from data.market_data import get_fundamentals
import os 
from dotenv import load_dotenv

load_dotenv()

def fundamental_analyst_node(state: ResearchState):
    ticker = state["ticker"]
    date = state["date"]
    
    with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client: 
        # makes the api call and produces a response object
        response = client.chat.send(
            model="openrouter/free", 
            messages=[
                {"role": "system", 
                 "content": "You are a highly regarded researcher for a Hedge Fund called "
                 "Senzo Trading tasked with analysing fundamental information from "
                 "the given date that is inputted about the company. Please write "
                 "a comprehensive report of the company's fundamental information "
                 "such as financial documents, company profile, basic company financials, and "
                 "company financial history to gain a broader view of the company's "
                 "fundamental information to inform traders. Make sure to include "
                 "as much detail as possible. Provide specific, actionable insights "
                 "with supporting evidence to help traders to make informed decisions. "
                 "Make sure to append a markdown table at the end of the report to "
                 "organise the key points in the report, organised and easy to read."
                 }
            ]
        )
        
    return {"fundamental_report": response.choices[0].messages.content}
