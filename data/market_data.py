import json
import warnings
import numpy as np
import pandas as pd
import yfinance as yf

import ta.momentum   as ta_mom
import ta.trend      as ta_trend
import ta.volatility as ta_vol
import ta.volume     as ta_volu

from datetime import date, timedelta
from typing import Optional

warnings.filterwarnings("ignore")

################################################################################

def get_fundamentals(ticker): 
    stock = yf.Ticker(ticker)
    company_info = stock.info
    company_financials = stock.financials
    company__balance_sheet = stock.balance_sheet
    company_cashflow = stock.cashflow
    return {
        "info": company_info,
        "financials": company_financials,
        "balance_sheet": company__balance_sheet,
        "cashflow": company_cashflow
    }

def price_history(ticker, start_date): 
    stock = yf.Ticker(ticker)
    company_history = stock.history(start=start_date, end=date.today())
    return company_history


################################################################################
#====================              MARKET NEWS             ====================#
################################################################################
# Fetch and structure recent news articles for a given ticker from Yahoo Finance.

def get_news(ticker):
    articles = yf.Ticker(ticker).news
    if not articles:
        return "No news found."
    
    items = []
    for item in articles:
        content = item.get("content", {})
        items.append(
            f"Title:  {content.get('title', 'N/A')}\n"
            f"Date:   {content.get('pubDate', 'N/A')}\n"
            f"Source: {content.get('provider', {}).get('displayName', 'N/A')}\n"
            f"URL:    {content.get('canonicalUrl', {}).get('url', 'N/A')}\n"
        )
    
    return "\n---\n".join(items)


################################################################################
#====================           MARKET TECHNICALS          ====================#
################################################################################
# Fetch OHLCV from Yahoo Finance and compute core technical indicators.

def _compute_indicators(d: pd.DataFrame) -> pd.DataFrame:
    """Compute all daily technical indicators and attach as columns."""
    d["EMA_20"] = ta_trend.EMAIndicator(d["Close"], window=20).ema_indicator()
    d["SMA_50"] = ta_trend.SMAIndicator(d["Close"], window=50).sma_indicator()
    d["SMA_200"] = ta_trend.SMAIndicator(d["Close"], window=200).sma_indicator()
    d["RSI"] = ta_mom.RSIIndicator(d["Close"], window=14).rsi()

    macd = ta_trend.MACD(d["Close"], window_slow=26, window_fast=12, window_sign=9)
    d["MACD_line"] = macd.macd()
    d["MACD_signal"] = macd.macd_signal()
    d["MACD_hist"] = macd.macd_diff()

    d["ATR"] = ta_vol.AverageTrueRange(
        d["High"], d["Low"], d["Close"], window=14).average_true_range()

    bb = ta_vol.BollingerBands(d["Close"], window=20, window_dev=2)
    d["BB_upper"] = bb.bollinger_hband()
    d["BB_middle"] = bb.bollinger_mavg()
    d["BB_lower"] = bb.bollinger_lband()
    d["BB_width"] = bb.bollinger_wband()

    d["OBV"] = ta_volu.OnBalanceVolumeIndicator(
        d["Close"], d["Volume"]).on_balance_volume()
    
    return d


def _fibonacci(df: pd.DataFrame, lookback: int = 60) -> dict:
    """Fibonacci retracements and extensions from the recent swing high/low."""
    recent     = df.tail(lookback)
    swing_high = float(recent["High"].max())
    swing_low  = float(recent["Low"].min())
    rng        = swing_high - swing_low
    return {
        "swing_high":      round(swing_high, 2),
        "swing_high_date": str(recent["High"].idxmax().date()),
        "swing_low":       round(swing_low, 2),
        "swing_low_date":  str(recent["Low"].idxmin().date()),
        "retracements": {
            "0.000": round(swing_low, 2),
            "0.236": round(swing_low + 0.236 * rng, 2),
            "0.382": round(swing_low + 0.382 * rng, 2),
            "0.500": round(swing_low + 0.500 * rng, 2),
            "0.618": round(swing_low + 0.618 * rng, 2),
            "0.786": round(swing_low + 0.786 * rng, 2),
            "1.000": round(swing_high, 2),
        },
        "extensions": {
            "1.272": round(swing_high + 0.272 * rng, 2),
            "1.618": round(swing_high + 0.618 * rng, 2),
            "2.618": round(swing_high + 1.618 * rng, 2),
        },
    }


def get_technicals(
    ticker:    str,
    date:      str,
    benchmark: str = "SPY",
) -> dict:
    """
    Fetch OHLCV from Yahoo Finance and compute core technical indicators.

    Args:
        ticker:    Stock ticker — use suffix for non-US (e.g. "CBA.AX", "RIO.L")
        date:      Analysis date "YYYY-MM-DD"
        benchmark: Benchmark ETF (default "SPY"; use "VAS.AX" for ASX stocks)

    Returns:
        Structured dict for injection into the TechnicalAnalyst agent prompt.
    """
    end   = pd.Timestamp(date)
    start = end - timedelta(days=730)

    # ── LOCAL HELPERS ─────────────────────────────────────────────────────────

    def fetch(sym: str, interval: str = "1d") -> pd.DataFrame:
        df = yf.Ticker(sym).history(
            start=start, end=end + timedelta(days=1), interval=interval)
        if df.empty:
            return df
        df.index = df.index.tz_convert(None)
        return df[df.index <= end]

    def ret(df: pd.DataFrame, n: int) -> Optional[float]:
        if len(df) < n + 1: return None
        return round((float(df["Close"].iloc[-1]) / 
                      float(df["Close"].iloc[-n - 1]) - 1) * 100, 2)

    def s(val, dec: int = 2) -> Optional[float]:
        try:
            v = float(val)
            return None if (np.isnan(v) or np.isinf(v)) else round(v, dec)
        except Exception:
            return None

    # ── DOWNLOAD ──────────────────────────────────────────────────────────────
    d = fetch(ticker)
    if d.empty:
        return {"error": f"No data for {ticker} — check ticker symbol."}

    d = _compute_indicators(d)

    w = fetch(ticker, interval="1wk")
    w["RSI"] = ta_mom.RSIIndicator(w["Close"], window=14).rsi()

    bench = fetch(benchmark)

    # ── SNAPSHOTS ─────────────────────────────────────────────────────────────
    latest = d.iloc[-1]
    prev = d.iloc[-2]
    w_last = w.iloc[-1]
    price = s(latest["Close"])

    # ── 52-WEEK RANGE ─────────────────────────────────────────────────────────
    d_52w = d[d.index >= end - timedelta(days=365)]
    h52 = round(float(d_52w["High"].max()), 2)
    l52 = round(float(d_52w["Low"].min()),  2)

    # ── PIVOT POINTS (inlined — called once) ─────────────────────────────────
    ph, pl, pc = float(prev["High"]), float(prev["Low"]), float(prev["Close"])
    P = (ph + pl + pc) / 3
    pivots = {
        "P":  round(P, 2),
        "R1": round(2 * P - pl, 2), 
        "R2": round(P + (ph - pl), 2), 
        "R3": round(ph + 2 * (P - pl), 2),
        "S1": round(2 * P - ph, 2), 
        "S2": round(P - (ph - pl), 2), 
        "S3": round(pl - 2 * (ph - P), 2),
    }

    # ── BB SQUEEZE ────────────────────────────────────────────────────────────
    bbw = d["BB_width"].tail(126).dropna()
    bb_squeeze = bool(
        len(bbw) > 20 and
        s(latest["BB_width"], 4) is not None and
        s(latest["BB_width"], 4) < float(bbw.mean() - bbw.std())
    )

    # ── OUTPUT ────────────────────────────────────────────────────────────────
    return {
        "meta": {
            "ticker": ticker, "date": date, "benchmark": benchmark,
        },
        "price": {
            "current": price,
            "52w_high": h52,
            "52w_low": l52,
            "pct_from_52w_high": round((price - h52) / h52 * 100, 2),
            "pct_from_52w_low": round((price - l52) / l52 * 100, 2),
        },
        "moving_averages": {
            "ema_20": s(latest["EMA_20"]),
            "sma_50": s(latest["SMA_50"]),
            "sma_200": s(latest["SMA_200"]),
        },
        "momentum": {
            "rsi_daily": s(latest["RSI"]),
            "rsi_weekly": s(w_last["RSI"]),
            "macd": {
                "line": s(latest["MACD_line"],   4),
                "signal": s(latest["MACD_signal"], 4),
                "histogram": s(latest["MACD_hist"],   4),
                "prev_histogram": s(prev["MACD_hist"],     4),
            },
        },
        "volatility": {
            "atr": s(latest["ATR"], 4),
            "atr_pct_of_price": s(float(s(latest["ATR"], 4) or 0) / price * 100, 2),
            "bb_upper": s(latest["BB_upper"]),
            "bb_middle": s(latest["BB_middle"]),
            "bb_lower": s(latest["BB_lower"]),
            "bb_bandwidth": s(latest["BB_width"], 4),
            "bb_squeeze": bb_squeeze,
        },
        "volume": {
            "latest": int(float(latest["Volume"])),
            "avg_20d": int(float(d["Volume"].tail(20).mean())),
            "vs_avg_20d_pct": round(
                (float(latest["Volume"]) - float(d["Volume"].tail(20).mean()))
                / float(d["Volume"].tail(20).mean()) * 100, 2
            ),
            "obv": s(latest["OBV"], 0),
            "obv_20d_ago": s(d["OBV"].iloc[-20], 0) if len(d) >= 20 else None,
        },
        "key_levels": {
            "pivot_points": pivots,
            "fibonacci": _fibonacci(d, lookback=60),
        },
        "relative_performance": {
            label: {
                "stock": (sr := ret(d, n)),
                "vs_benchmark": round(sr - ret(bench, n), 2) if sr 
                and ret(bench, n) else None,
            }
            for label, n in [("30d", 21), ("90d", 63)]
            if ret(d, n) is not None
        },
        "ohlcv": {
            "daily_last_15": {
                str(ts.date()): {"O": s(r["Open"]), "H": s(r["High"]), 
                                 "L": s(r["Low"]), "C": s(r["Close"]), 
                                 "V": int(r["Volume"])}
                for ts, r in d.tail(15).iterrows()
            },
            "weekly_last_26": {
                str(ts.date()): {"O": s(r["Open"]), "H": s(r["High"]), 
                                 "L": s(r["Low"]), "C": s(r["Close"]), 
                                 "V": int(r["Volume"])}
                for ts, r in w.tail(26).iterrows()
            },
        },
    }


def technicals_to_str(technicals: dict) -> str:
    # Serialise for injection into the agent user prompt
    return json.dumps(technicals, indent=2, default=str)