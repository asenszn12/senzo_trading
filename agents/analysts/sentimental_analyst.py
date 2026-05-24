from graph.state import ResearchState
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

def sentimental_analyst_node(state: ResearchState):
    ticker = state["ticker"]
    date = state["ticker"]
    sentimental = 0 

    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getev('OPENROUTER_API_KEY')}", 
            "Content-Type":"application/json"
        } ,
        json={
            "model": "openrouter/free", 
            "messages": [
                {"role": "system", "content": "system_prompt"}, 
                {"role": "user", "content": "user_prompt"}
            ]
        } )


    result = response.json()["choices"][0]["messages"]["content"]
    return {"sentimental_report": result}

