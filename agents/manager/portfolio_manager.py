import sys 
from pathlib import Path 
current_file = Path(__file__).resolve()
for parent in current_file.parents:
    if parent.name == "senzo_trading":
        sys.path.append(str(parent))
        break
from graph.state import ResearchState
from agents.run_task import run_task 

sys_prompt = """
## ROLE
You are the Portfolio Manager at Senzo Trading. You receive the research manager's 
verdict and the trader's proposed strategy. You have the final say on whether to 
buy or not buy the stock. Be decisive. Ground every conclusion in specific evidence 
from the inputs provided.

---
## HARD CONSTRAINTS
- Your decision must be Buy or Do Not Buy. No sitting on the fence.
- Reference specific arguments and metrics from both inputs.
- No fabrication. Only use what has been provided.
- Do not re-argue the bull or bear case — that debate is closed.
- Use Australian English spelling conventions.

---
## OUTPUT — always in this order

### PORTFOLIO MANAGEMENT DECISION

**Decision: Buy / Do Not Buy**
[One sentence explaining the decision.]

---

### KEY ARGUMENTS SUMMARISED

**Research Manager:**
- [Key point 1]
- [Key point 2]
- [Key point 3]

**{trader_profile} Trader:**
- [Key point 1]
- [Key point 2]
- [Key point 3]

---

### RATIONALE
1. [Reason]
2. [Reason]
3. [Reason]
4. [Reason — if applicable]
5. [Reason — if applicable]

---

### REFINED STRATEGY
[If Buy — entry conditions from trader strategy and when to revisit.]
[If Do Not Buy — what conditions would change this and when to revisit.]

---

### CONVICTION SCORE
| Field | Value |
|-------|-------|
| Decision | Buy / Do Not Buy |
| Conviction | High / Medium / Low |
| Key Risk | [biggest thing that could make you wrong] |
| Revisit Trigger | [what would change this decision] |
"""

def portfolio_manager_node(state: ResearchState):
    # getting all info from relevant sources - research manager and trader_node 
    ticker = state["ticker"]
    research_verdict = state["research_verdict"]
    trader_strategy = state["trader_strategy"]
    

    user_prompt = f"""Produce the portfolio manager's final report using 
    research managers investment plan: {research_verdict} and the traders 
    transaction proposal: {trader_strategy}
    """ 

    result = run_task(system=sys_prompt, user=user_prompt)
    return {"manager_recc": result}


if __name__ == "__main__":
    from agents.analysts.fundamental_analyst import fundamental_analyst_node
    from agents.analysts.sentimental_analyst import sentimental_analyst_node
    from agents.analysts.news_analyst import news_analyst_node
    from agents.analysts.technical_analyst import technical_analyst_node
    from agents.researchers.research_debate import research_debate_node
    from agents.manager.research_manager import research_manager_node 
    from agents.trader.trader import conservative_trader_node 

    state = {
        "ticker": "AAPL",
        "date": "2026-01-01",
        "benchmark": "SPY",
        "trader_strategy": "conservative"
    }

    state.update(fundamental_analyst_node(state))
    state.update(sentimental_analyst_node(state))
    state.update(news_analyst_node(state))
    state.update(technical_analyst_node(state))
    # call the other analysts to make the research debate avaliable 
    state.update(research_debate_node(state))
    state.update(research_manager_node(state))
    state.update(conservative_trader_node(state))

    # testing using the conservative trader node 
    result = portfolio_manager_node(state)
    print(result)