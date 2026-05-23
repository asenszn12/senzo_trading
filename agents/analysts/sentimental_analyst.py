from graph.state import ResearchState
from openrouter import OpenRouter 
import os 

def sentimental_analyst_node(state: ResearchState):
    with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client: 
        # makes the api call and produces a response object
        response = client.chat.send(
            model="openrouter/free", 
            messages=[
                {"role": "system", 
                 "content":"You are a Sentimental analyst for Hedge Fund called "
                 "Senzo Trading"}
            ]
        )
        
    return {"sentimental_analyst": response.choices[0].messages.content}

