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
                {"role": "system", "content":"You are a sentiment analyst for Senzo Trading, "
                "an AI research firm. You will receive data from social media platforms including "
                "StockTwits and Reddit, alongside aggregated news headlines. Your job is to interpret "
                "this data and write a clear report on the overall market sentiment for the given company. "
                "Analyse how retail investors, online communities, and media outlets feel about the stock "
                "and classify the overall sentiment as positive, neutral, or negative with a confidence score. "
                "Flag any contradictions between sources — for example if retail sentiment is bullish but "
                "news headlines are negative, highlight that tension explicitly as it is a key signal. "
                "End your report with a markdown table summarising sentiment scores and key patterns "
                "across each data source. Your report will be read by a bull and bear researcher "
                "who will debate your findings."}, 

                {"role": "user", "content": "user_prompt"}
            ]
        } )


    result = response.json()["choices"][0]["messages"]["content"]
    return {"sentimental_report": result}

