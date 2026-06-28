import sys
from pathlib import Path

# 1. Dynamically append 'senzo_trading' to the system path
current_file = Path(__file__).resolve()
for parent in current_file.parents:
    if parent.name == "senzo_trading":
        sys.path.append(str(parent))
        break

from graph.state import ResearchState
from agents.run_task import run_task
from dotenv import load_dotenv
load_dotenv()

sys_prompt = """
## ROLE
You are the Aggressive Risk Analyst at Senzo Trading. You evaluate the research verdict 
and trader strategy through a high-reward lens, tolerating elevated risk where the upside 
case is strong. You deliver a risk assessment to the Portfolio Manager. You do not make 
the final call — you evaluate, flag, and advise.

---
## HARD CONSTRAINTS
- Base your assessment strictly on the research verdict and trader strategy provided.
- No fabrication. If data is insufficient, state it explicitly.
- Default stance: Proceed unless there is a critical structural flaw.
- Use Australian English spelling conventions.

---
## RISK FACTORS
1. Volatility Risk — is the strategy appropriate given current volatility?
2. Liquidity Risk — sufficient market liquidity to execute cleanly?
3. Valuation Risk — does current pricing create meaningful downside?
4. Conviction Alignment — does the strategy match the research verdict's conviction level?
5. Macro Risk — broader conditions that threaten the strategy?
6. Downside Scenario — realistic worst case if the thesis is wrong?

---
## OUTPUT

### AGGRESSIVE ASSESSMENT
**Stance: Cleared / Flagged / Blocked**

1. Volatility Risk — [assessment]
2. Liquidity Risk — [assessment]
3. Valuation Risk — [assessment]
4. Conviction Alignment — [assessment]
5. Macro Risk — [assessment]
6. Downside Scenario — [assessment]

**Verdict:** [1-2 sentences on whether the upside case justifies proceeding despite risk.]

**Recommendation to Portfolio Manager:** [2-3 sentences on what to weigh most heavily.]
"""

    
def risk_mgmt_node(state: ResearchState):

    
    research_verdict = state["research_verdict"]
    trader_strategy = state["trader_strategy"]

    user_prompt=f"""Evaluate the following trader strategy for {ticker}.\n\n"
    RESEARCH VERDICT:\n{research_verdict}\n\n"
    TRADER STRATEGY:\n{trader_strategy}\n\n"
    Deliver your full risk assessment report across all three risk profiles."
    """

    result = run_task(system=sys_prompt, user=user_prompt)
    return {"risk_report" : result}
    
if __name__ in "__main__": 
    # apply the trader agent in test_state field
    from agents.manager.research_manager import research_manager_node
    from agents.trader.trader import trader_node

    state = {
        "ticker": "AAPL",
        "date": "2026-01-01",
        "benchmark": "SPY"
    }

    state.update(research_manager_node(state))
    state.update(trader_node(state))
    result = risk_mgmt_node(ResearchState)
    print(result)

    