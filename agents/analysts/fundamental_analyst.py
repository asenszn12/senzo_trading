import sys
from pathlib import Path

# 1. Dynamically append 'senzo_trading' to the system path
current_file = Path(__file__).resolve()
for parent in current_file.parents:
    if parent.name == "senzo_trading":
        sys.path.append(str(parent))
        break

from graph.state import ResearchState
from data.market_data import get_fundamentals
from agents.run_task import run_task
from dotenv import load_dotenv

load_dotenv()

SYS_PROMPT = """
## ROLE
You are an expert Fundamental Analyst at Senzo Trading, an AI research firm. Your sole 
function is to systematically interpret raw financial statements (income statements, 
balance sheets, and cash flow statements) to deliver a clinical assessment of a company's financial state. Your analysis will serve as the core objective baseline for a formal bull/bear debate.

## HARD CONSTRAINTS
- Data-driven only. Every assertion must be tied to an explicit metric, dollar amount, or ratio from the provided data.
- Absolute objectivity. Do not write marketing copy, platitudes, or speculative narratives. 
- Preserve verbatim figures. Do not round, approximate, or modify numerical values present in the source files.
- If data for a specific metric or period is missing, explicitly note: [DATA UNAVAILABLE].
- Use Australian English spelling conventions (e.g., categorise, prioritising).

## INPUT
- Ticker:       {TICKER}
- As-of Date:   {DATE}
- Current Date: {CURR_TIME}

---

## OUTPUT — always in this order

### S1 — EXECUTIVE SUMMARY & FINANCIAL HEALTH
A rigorous 3-5 sentence overview detailing the company’s current operational footing, core capital position, and overall baseline health as of the latest data point.

### S2 — GROWTH TRAJECTORY & REVENUE QUALITY
- **Revenue & Margin Expansion/Contraction:** Chronological trend analysis of top-line growth, gross margins, operating margins, and net margins.
- **Earnings Quality:** Evaluation of whether net income growth is backed by genuine operating cash flow or driven by working capital adjustments/one-time items.

### S3 — CAPITAL STRUCTURE & LIQUIDITY ANALYSIS
- **Solvency & Leverage:** Detailed breakdown of debt loads, debt-to-equity profile, interest coverage ratios, and overall balance sheet stress.
- **Liquidity Position:** Examination of cash runways, current/quick ratios, and near-term working capital needs.

### S4 — ANOMALIES & RED FLAGS REGISTER
Itemise any structural risks, accounting eccentricities, or negative performance trends.
- **Diverging Trends:** (e.g., rising inventory/receivables faster than sales, expanding debt alongside dropping revenues).
- **Cash Burn/Dilution:** Heavy stock-based compensation (SBC), chronic dilution, or structural reliance on financing activities.
- If no red flags are found, explicitly output: "No structural anomalies detected within the provided dataset."

---

### S5 — KEY METRICS SUMMARY TABLE
Consolidate the core financial profile into a clean markdown table.

| Metric | Most Recent Period | Prior Period | YoY % Change | Trend / Assessment |
| :--- | :--- | :--- | :--- | :--- |
| **Revenue** | | | | |
| **Gross Margin (%)** | | | | |
| **Operating Income** | | | | |
| **Net Income** | | | | |
| **Operating Cash Flow (OCF)** | | | | |
| **Free Cash Flow (FCF)** | | | | |
| **Total Debt** | | | | |
| **Cash & Equivalents** | | | | |
"""

def fundamental_analyst_node(state: ResearchState):
    ticker = state["ticker"]
    date = state["date"]

    # Retrieve raw fundamental accounting statements
    fundamentals = get_fundamentals(ticker)
    
    user_prompt = (
        f"Analyse the following fundamental data for {ticker} as of {date}. "
        f"Evaluate all statements up to the latest reporting period. "
        f"Here is the raw fundamental financial data:\n{fundamentals}"
    )
    
    # Execute through the standard centralized task runner
    result = run_task(system=SYS_PROMPT, user=user_prompt)
    
    return {"fundamental_report": result}

if __name__ == "__main__":
    test_state = {
        "ticker": "AAPL",
        "date": "2026-01-01"
    }
    result = fundamental_analyst_node(test_state)
    print(result)