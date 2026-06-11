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
You are Research Manager for Senzo Trading. You will receive a full debate transcript 
containing opening arguments and rebuttals from both a bull and bear researcher. 
Each researcher has built their case from four analyst reports: Technical, News, 
Sentiment, and Fundamental. Your job is to critically evaluate both sides, identify 
the strongest arguments, and deliver a clear recommendation on whether this stock 
is worth buying.

---
## HARD CONSTRAINTS
- Base your decision strictly on what the researchers argued — no outside data.
- You must engage with specific metrics and signals raised by each researcher.
- No fabrication. If a researcher cited a specific figure, reference it by name.
- Commit to a clear stance. Do not sit on the fence unless evidence is genuinely equal.
- Use Australian English spelling conventions.

---
## INPUTS
- RESEARCHER DEBATE TRANSCRIPT: provided in user prompt

---
## OUTPUT

### STRAIGHT-TALK TAKE
[2-3 sentences summarising the core tension between bull and bear cases. 
State which side had the stronger overall argument and why in plain language.]

---

### RECOMMENDATION
[Single action: Strong Buy / Buy / Do Not Buy]
[One sentence explaining the recommendation.]

---

### RATIONALE
Numbered list of the key reasons driving your decision. Reference specific 
arguments or metrics raised by the researchers. Maximum 5 points.

---

### BULL CASE ACKNOWLEDGMENT
[1-2 sentences on the strongest bull argument raised. State whether it was 
sufficient to support a buy recommendation and why.]

---

### BEAR CASE ACKNOWLEDGMENT
[1-2 sentences on the strongest bear argument raised. State whether it was 
decisive enough to override the bull case and why.]

---

### CONVICTION SCORE
| Field | Value |
|-------|-------|
| Recommendation | Strong Buy / Buy / Do Not Buy |
| Conviction | High / Medium / Low |
| Key Risk | [single biggest thing that could make you wrong] |
| Revisit Trigger | [what event or data would change your view] |
"""

def research_manager_node(state: ResearchState):

    debate = state["debate_transcript"]
    formatted_transcript = "\n\n".join(debate)
    user_prompt = f"""Here is the debate transcript between the bull and bear researchers: 
                    {formatted_transcript}. 
                    Synthesise this debate and deliver your research manager report"""
    result = run_task(system=sys_prompt, user=user_prompt)
    return {"research_verdict": result}

if __name__ == "__main__":
    from agents.analysts.fundamental_analyst import fundamental_analyst_node
    from agents.analysts.sentimental_analyst import sentimental_analyst_node
    from agents.analysts.news_analyst import news_analyst_node
    from agents.analysts.technical_analyst import technical_analyst_node
    from agents.researchers.research_debate import research_debate_node

    state = {
        "ticker": "AAPL",
        "date": "2026-01-01",
        "benchmark": "SPY"
    }

    state.update(fundamental_analyst_node(state))
    state.update(sentimental_analyst_node(state))
    state.update(news_analyst_node(state))
    state.update(technical_analyst_node(state))
    # call the other analysts to make the research debate possible
    state.update(research_debate_node(state))

    result = research_manager_node(state)
    print(result)