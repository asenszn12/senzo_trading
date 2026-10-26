# Senzo TRF: Multi-Agentic Trading Research Framework

**Senzo TRF** is a multi-agentic trading research framework that analyses a stock through parallel specialist analysts, a structured bull versus bear debate, and an advisory panel that delivers a final verdict. Every step is written out in plain language, so you can read exactly why the system reached its recommendation.

Senzo stops at the recommendation. It does not connect to a broker and it never places trades. What you do with the verdict is entirely up to you.

> **Inspiration and acknowledgements**
> Senzo takes inspiration from [Tauric Research's TradingAgents](https://github.com/TauricResearch/TradingAgents). If you are interested in multi-agent trading systems, their repository and research are well worth a look.

> **Disclaimer**
> Senzo is a research and learning tool. Nothing it produces is financial advice. Language models can be wrong, data sources can be incomplete, and past performance does not predict future results. Do your own research before making any financial decision.

---

## How it works

```
Analyst team (run in parallel)
  Fundamentals | Sentiment | News | Technical
            ↓
Bull and bear researcher debate
  (opening arguments, then rebuttals)
            ↓
Research manager
  (weighs both sides, picks a stance)
            ↓
Trader
  (strategy adjusted to your risk profile)
            ↓
Portfolio manager
  (final Buy / Do Not Buy decision)
```

### 1. Analyst team

| Analyst | What it looks at |
|---|---|
| **Fundamentals** | Income statements, balance sheets, cash flow, valuation metrics |
| **Sentiment** | Reddit discussion (r/wallstreetbets, r/stocks, r/investing, r/stockmarket) alongside news headlines, flagging where retail and media views disagree |
| **News** | Recent headlines sorted into categories such as earnings, regulatory and legal, analyst activity and macro events |
| **Technical** | Trend structure, key levels, RSI, MACD, moving averages, volume, volatility and multi-timeframe alignment against a benchmark |

### 2. Bull and bear debate

Two researchers read the same four reports. One builds the strongest bullish case, the other the strongest bearish case. Both write their opening arguments at the same time, then each writes a rebuttal after reading the other's opening. Running the openings in parallel stops either side gaining an advantage from speaking first.

### 3. Advisory panel

- **Research manager:** reads the debate, acknowledges the strongest points from each side and commits to a recommendation (Strong Buy, Buy or Do Not Buy).
- **Trader:** turns that verdict into a concrete plan with entry levels, targets, stops and invalidation conditions. The plan is shaped by the risk profile you choose.
- **Portfolio manager:** makes the final call (**Buy** or **Do Not Buy**) with a rationale, a refined strategy and a conviction score.

### Risk profiles

You choose a profile at the start of each run.

| Profile | Approach |
|---|---|
| **Conservative** | Only high-quality setups, at least 2:1 risk/reward, no chasing breakouts, stands aside if signals conflict |
| **Neutral** | Balanced, at least 1.5:1 risk/reward, accepts one conflicting signal if the main driver is strong |
| **Aggressive** | Accepts lower-quality setups and 1:1 risk/reward at high conviction, breakout entries allowed |

---

## Quick start

You will need an OpenRouter API key. Get one at [openrouter.ai](https://openrouter.ai). (If you want, you can set a limit for your API key as well in the rare chance you may get charged).

### Option A: Run with Python (recommended)

Requires Python 3.10 or newer.

```bash
git clone https://github.com/asenszn12/senzo_trading.git
cd senzo_trading

cp .env.example .env
```

Open `.env` and paste in your own OpenRouter API key, then:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

On Windows PowerShell:

```powershell
copy .env.example .env
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

### Option B: Run with Docker

You only need Docker Desktop installed.

```bash
git clone https://github.com/asenszn12/senzo_trading.git
cd senzo_trading

cp .env.example .env
docker compose build
docker compose run --rm -it server
```

The `-it` flag matters because Senzo is an interactive terminal app.

---

## Using Senzo

When you run `main.py` it walks you through three steps:

1. **Ticker:** for example `AAPL`, `TSLA` or `SPY`.
2. **Analysis date:** entered as `DD-MM-YYYY`.
3. **Risk profile:** pick one with the arrow keys and press Enter.

A progress table tracks each agent as it works. When the run finishes, every report is printed in order: analyst reports, the debate, the research manager's verdict, the trader's strategy and the final recommendation.

---

## Configuration

Your `.env` file holds your settings. It must never be committed to Git.

```
# Get your API key from https://openrouter.ai
OPENROUTER_API_KEY=your_key_here

# If you want to use a more powerful model or if you are hitting free-tier rate limits, you can edit the code directly:
1. Open `agents/run_task.py`
2. Locate line 12: `"model": "openrouter/free"`
3. Change `"openrouter/free"` to your desired OpenRouter model ID.
```

If `OPENROUTER_MODEL` is not set, Senzo uses OpenRouter's free model router. Free models are rate limited, and a full run makes a lot of calls, so you may hit limits. Pinning a specific model gives more consistent results.

---

## Project structure

```
senzo_trading/
├── main.py              # terminal interface and entry point
├── agents/
│   ├── analysts/        # fundamentals, sentiment, news, technical
│   ├── researchers/     # bull and bear debate
│   ├── manager/         # research manager, portfolio manager
│   ├── trader/          # conservative, neutral and aggressive traders (all under a single file)
│   └── run_task.py      # shared helper for calling the language model
├── graph/
│   ├── state.py         # shared state passed between agents
│   └── graph.py         # LangGraph pipeline wiring
└── data/
    ├── market_data.py   # prices, fundamentals, technical data, news
    └── sentiment_data.py
```

Senzo is built on [LangGraph](https://github.com/langchain-ai/langgraph) for orchestration, with data from yfinance and Reddit, and models accessed through OpenRouter.

---

## Known limitations

- **Data "freshness":** News and Reddit sources only expose a limited recent window, so older analysis dates may return little or no news. Price and fundamental data respect the date you choose.
- **Rate limits:** Since the application itself runs on the openrouter/free models, these free OpenRouter models allow a limited number of requests per minute and per day.
- **Model quality varies:** Output quality and speed depends on the model you use from the openrouter/free router. Always read the reasoning rather than just the final verdict.
- **No execution:** By design, Senzo never trades on your behalf.

---

## Credits

Built by Aadhi Senthil Kumar ([asenszn12](https://github.com/asenszn12)) and Sean Enzo Nebres ([sean-25](https://github.com/sean-25)).
