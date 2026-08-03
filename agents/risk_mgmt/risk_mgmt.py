from graph.state import ResearchState
from agents.run_task import run_task
from langgraph.types import interrupt


RISK_TYPES = ["conservative", "neutral", "aggressive"]

sys_prompt = """
You are assessing a user's investment risk profile.

Based on their response, classify them in ONE WORD 
as EXACTLY one of:
conservative, neutral, aggressive.

Consider:
- How much loss they are comfortable with
- Their investment horizon  
- Their return expectations
- Their reaction to market volatility

If unclear, default to neutral.
"""

def risk_profile_node(state: ResearchState):
    
    risk_description = interrupt(
        "Describe your investment risk profile, such as "
        "your comfort with loss, investment horizon, return expectations, "
        "Highlight your goals, preferences, concerns and other factors that "
        "shape your investment approach."
    )
    profile = run_task(system=sys_prompt, user=risk_description)
    if profile not in RISK_TYPES:
        profile = "neutral"
    return {"risk_profile": profile}


def route_trader(state: ResearchState):
    return state.get("risk_profile")