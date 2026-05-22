from graph.state import ResearchState
from openrouter import OpenRouter 
import os 


def fundamental_analyst_node(state: ResearchState):
    with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client: 
        # makes the api call and produces a response object
        response = client.chat.send(
            model="openrouter/free", 
            messages=[
                {"role": "system", 
                 "content":"You are a Fundamentals analyst for Hedge Fund"}
            ]
        )
        
    return {"fundamental_report": response.choices[0].message.content}
