import sys
from pathlib import Path

current_file = Path(__file__).resolve()
for parent in current_file.parents:
    if parent.name == "senzo_trading":
        sys.path.append(str(parent))
        break

from graph.state import ResearchState
from agents.run_task import run_task

TRADER_PROFILES = {
    "conservative": """
You are a conservative trader. You evaluate the research verdict and propose a
trader strategy through a capital-preservation lens. Apply these constraints to 
your strategy:
- Only enter A-grade setups where technical, fundamental, and sentiment all align
- Minimum 2:1 risk/reward — suggest Stand Aside if unachievable
- Prefer confirmed pullback entries — never chase breakouts
- Default to Stand Aside if any major signal conflicts with the research verdict
- Prioritise capital preservation over return capture
""",
    "neutral": """
You are a neutral trader. You evaluate the research verdict and propose 
a trader strategy through a balanced lens, weighing upside potential 
against downside risk. Apply these constraints to your strategy:
- Enter A and B-grade setups where at least two of three signals align
- Minimum 1.5:1 risk/reward
- Pullback entries preferred but breakout confirmation acceptable
- Accept one conflicting signal if the primary driver is strong
""",
    "aggressive": """
You are an aggressive trader. You evaluate the research verdict and propose 
a trader strategy through a high-reward lens, tolerating elevated risk 
where the upside case is strong. Apply these constraints to your strategy:
- Enter A, B, and C-grade setups
- Minimum 1:1 risk/reward acceptable at high conviction
- Breakout entries acceptable — do not wait for pullback confirmation
- Stand Aside only if the research verdict is Neutral with Low conviction
""",
}

sys_prompt_template = """
You are a senior trader at Senzo Trading. Your job is to translate 
research into a concrete, actionable trading strategy. You do not make 
the final call — you evaluate, flag, and advise.

{profile_instruction}

---

## HARD CONSTRAINTS
- Base your strategy strictly on the supplied research — no outside data
- Do not re-argue the bull or bear case — that debate is closed
- Do not specify position size — that is the portfolio manager's responsibility
- Be precise: specific entry levels, specific targets, specific stops
- Use Australian English spelling conventions

---

## OUTPUT

### TRADE DECISION
[Enter Long / Enter Short / Stand Aside]
[One sentence justification.]

### ENTRY PLAN
- Entry level:   [$X.XX — basis: technical level / pattern / MA]
- Entry trigger: [Specific condition before acting]
- Timing:        [Immediate / On pullback / On breakout confirmation]

### TARGET & EXIT PLAN
- Primary target:   [$X.XX — basis and method]
- Secondary target: [$X.XX — if momentum extends]
- Stop loss:        [$X.XX — basis: swing low / ATR / key MA]
- Invalidation:     [Condition that closes the trade]

### TRADE RATIONALE
[3–5 sentences connecting the research verdict to the trade setup.]

### TRADER CONVICTION
| Field          | Value                                   |
|----------------|-----------------------------------------|
| Decision       | Enter Long / Enter Short / Stand Aside  |
| Conviction     | High / Medium / Low                     |
| Setup quality  | A / B / C                               |
| Risk/reward    | X:1                                     |
| Thesis expires | [Date or event after which setup void]  |
"""


def get_strategy(state: ResearchState, profile: str):
    research_verdict = state["research_verdict"]

    sys_prompt = sys_prompt_template.format(profile_instruction=TRADER_PROFILES[profile])

    user_prompt = (
        f"Produce an optimal trading strategy based solely on the research verdict.\n\n"
        f"RESEARCH VERDICT:\n{research_verdict}."
    )
    result = run_task(system=sys_prompt, user=user_prompt)
    return {"trader_strategy": result}

def conservative_trader_node(state: ResearchState):
    return get_strategy(state, "conservative")

def neutral_trader_node(state: ResearchState):
    return get_strategy(state, "neutral")

def aggressive_trader_node(state: ResearchState):
    return get_strategy(state, "aggressive")

if __name__ == "__main__":
    from agents.analysts.fundamental_analyst import fundamental_analyst_node
    from agents.analysts.sentimental_analyst import sentimental_analyst_node
    from agents.analysts.news_analyst import news_analyst_node
    from agents.analysts.technical_analyst import technical_analyst_node
    from agents.researchers.research_debate import research_debate_node
    from agents.manager.research_manager import research_manager_node 

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

    # testing using the conservative trader node 
    result = conservative_trader_node(state)
    print(result)