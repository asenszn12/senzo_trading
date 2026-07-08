from typing import TypedDict

class ResearchState(TypedDict):
    ticker: str
    date: str 
    benchmark: str

    # analyst reports
    fundamental_report: str 
    sentimental_report: str 
    news_report: str 
    technical_report: str 

    # transcript between bullish and bearish researchers 
    debate_transcript: list 
    # research manager verdict
    research_verdict: str

    # risk profile report
    risk_profile: str

    # trader strategy dependent on risk profile (conservative, neutral, aggressive)
    trader_strategy: str
    
    # manager final recommendation 
    manager_recc: str 


