from typing import TypedDict

class ResearchState(TypedDict):
    ticker: str
    date: str 
    # each analyst report 
    fundamental_report: str 
    sentimental_report: str 
    news_report: str 
    technical_report: str 
    # transcript between bullish and bearish researchers 
    debate_transcript: list 
    # research manager verdict
    research_verdict: str
    # trader agent report 
    trader_strategy: str 
    # risk management report (deciding whether to account for aggressive, neutral and conservative)
    risk_report: str 
    # manager final recommendation 
    manager_recc: str 


