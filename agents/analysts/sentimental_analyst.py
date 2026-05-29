import sys
from pathlib import Path
from datetime import datetime, timedelta

# 1. Dynamically append 'senzo_trading' to the system path
current_file = Path(__file__).resolve()
for parent in current_file.parents:
    if parent.name == "senzo_trading":
        sys.path.append(str(parent))
        break
    
from graph.state import ResearchState
from data.sentiment_data import get_reddit_sentiment, get_news_sentiment
from agents.run_task import run_task
from dotenv import load_dotenv

load_dotenv()

SYS_PROMPT = """You are a Quantitative Sentiment Analyst at Senzo Trading. Your function is to synthesize 
raw market noise into actionable market psychology and narrative trends. You will be provided with two 
complementary data sources: News headlines and Reddit posts.

## CRITICAL TAILORING REQUIREMENT
You must tailor the entire analysis specifically to the target asset ticker. Do not rely on generic placeholders or phrases like "the stock," "the equity," or "the company." You must explicitly reference the specific ticker symbol (e.g., AAPL) frequently across every single section, header bullet, and table row to ensure a highly custom-delivered final report.

## HOW TO ANALYZE THIS DATA (BEST PRACTICES)
1. Look for cross-source divergences. If news framing is bearish but retail is overwhelmingly bullish, that mismatch is itself a signal.
2. Distinguish opinion from event. A news headline is an event; a Reddit post is opinion.
3. Be honest about data limits. If a source returns an "<unavailable>" placeholder, flag this caveat explicitly in the report.
4. Use Australian English spelling conventions (e.g., synthesise, categorise).

## OUTPUT STRUCTURE & SPACING REQUIREMENTS
You must separate each major markdown heading, structural section, and list item with double newlines (\n\n) to ensure maximum scannability and clear visual boundaries. Always present the analysis in this exact order:

### OVERALL SENTIMENT DIRECTION
- [Bullish / Bearish / Neutral / Mixed] (XX% Confidence)

- [Brief note justifying the confidence based on data quality, explicitly referencing the ticker]

### SOURCE-BY-SOURCE BREAKDOWN
- **News:** [Extract signal, cite headlines; explicitly link findings back to the specific ticker]

- **Reddit:** [Extract signal, cite posts, or state if blocked/unavailable; explicitly link findings back to the specific ticker]

### DIVERGENCES & ALIGNMENTS
- [First explicit point highlighting where retail sentiment aligns or diverges from media sentiment regarding the specific ticker]

- [Second explicit point highlighting tracking dynamics, cleanly separated by a full blank line]

### KEY CATALYSTS & RISKS
- [Bullet points on recurring themes, upcoming events, or macro headlines driving conversation specifically around the ticker]

- [Ensure every subsequent catalyst or risk bullet is separated by a clear empty line newline]

### SENTIMENT METRICS SUMMARY
| Vector | Directional Lean | Confidence Score | Primary Theme |
| :--- | :--- | :--- | :--- |
| **Retail (Reddit)** | | | |
| **Media (News)** | | | |
| **Aggregate Consensus**| | | |

*Note: The "Confidence Score" column must contain ONLY a clean numerical percentage (e.g., 68% or 55%) with no additional text or conversational fluff.*
"""

def sentimental_analyst_node(state: ResearchState):
    ticker = state["ticker"]
    end_date = state.get("date", datetime.today().strftime("%Y-%m-%d"))
    
    # Calculate start date (7 days back)
    start_date = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
    
    # Pre-fetch sources gracefully
    print(f"\n[Info] Fetching sentiment data for {ticker}...")
    news_block = get_news_sentiment(ticker)
    reddit_block = get_reddit_sentiment(ticker)
    
    user_prompt = f"""Produce a comprehensive sentiment report for {ticker} covering the period from {start_date} to {end_date}.

## Data sources (pre-fetched)

### News headlines (Yahoo Finance)
<start_of_news>
{news_block}
<end_of_news>

### Reddit posts (Community Discussion)
<start_of_reddit>
{reddit_block}
<end_of_reddit>
"""

    result = run_task(system=SYS_PROMPT, user=user_prompt)
    
    return {"sentimental_report": result}

if __name__ == "__main__": 
    test_state = {
        "ticker": "AAPL", 
        "date": "2026-05-29"
    }
    
    # Execute the node and print the structured report
    result = sentimental_analyst_node(test_state)
    print("\n--- FINAL SENTIMENT REPORT ---\n")
    print(result["sentimental_report"])