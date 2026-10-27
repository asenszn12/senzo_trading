from rich.console import Console, Group
from rich.panel import Panel
from rich.markdown import Markdown
from rich.align import Align
from rich.live import Live
from rich.table import Table
from rich.spinner import Spinner
import questionary
from datetime import datetime

console = Console()

# Senzo TRF specific block ASCII logo
ascii_logo = r"""
  _____                       _______ _____  ______ 
 / ____|                     |__   __|  __ \|  ____|
| (___   ___ _ __  ___  ___     | |  | |__) | |__   
 \___ \ / _ \ '_ \|_  // _ \    | |  |  _  /|  __|  
 ____) |  __/ | | |/ /| (_) |   | |  | | \ \| |     
|_____/ \___|_| |_/___|\___/    |_|  |_|  \_\_|     
"""

def bad(text):
    t = (text or "").strip()
    return len(t) < 200 or t.startswith("User Safety:")

def run_step(node, state, retries=1):
    for _ in range(retries + 1):
        out = node(state)
        values = [x for v in out.values() for x in (v if isinstance(v, list) else [v])]
        if not any(bad(v) for v in values):
            return out
    return out

def main():
    # 1. Main Header Panel with centered Group elements
    header_group = Group(
        Align.center(f"[bold blue]{ascii_logo}[/bold blue]"),
        Align.center("[bold green]Senzo TRF: a multi-agentic research framework for trading.[/bold green]\n"),
        Align.center("[bold][underline]Workflow Steps:[/bold][/underline]\n"),
        Align.center("[italic]Analyst team (fundamentals, sentiment, news, and technical) ➔  Bullish and Bearish researcher debate ➔  Research manager ➔  Trader (risk-adjusted) ➔  Portfolio manager[/italic]\n\n"),
        Align.center("[dim]Built by Aadhi Senthil Kumar (github.com/asenszn12) and Sean Enzo Nebres (github.com/sean-25)[/dim]\n")
    )

    console.print(
        Panel(
            header_group, 
            border_style="green", 
            title="Welcome to Senzo Trading", 
            subtitle="Multi-Agentic Research Framework for Trading"
        )
    )

    # 2. Step 1: Ticker Box
    console.print(
        Panel(
            "Enter the ticker symbol you want to analyze.\n"
            "[dim]Example: AAPL, TSLA, SPY[/dim]\n"
            "[dim yellow]* Note: Please ensure you input a valid, correct stock ticker (1 to 5 characters).[/dim yellow]", 
            title="[bold]Step 1: Ticker Symbol[/bold]", 
            title_align="left", 
            border_style="blue"
        )
    )
    
    # Validation loop for Ticker
    while True:
        ticker = console.input("[bold cyan]> [/bold cyan]").strip().upper()
        if 0 < len(ticker) <= 5:
            break
        console.print("[bold red]Invalid input![/bold red] Ticker must be between 1 and 5 characters. Please try again.")

    # 3. Step 2: Date Box
    console.print(
        Panel(
            "Set the analysis date you want to get information from (DD-MM-YYYY).", 
            title="[bold]Step 2: Analysis Date[/bold]", 
            title_align="left", 
            border_style="blue"
        )
    )
    
    # Validation loop for Date
    while True:
        date_input = console.input("[bold cyan]> [/bold cyan]").strip()
        try:
            # Strictly validate DD-MM-YYYY format and ensure it's a valid calendar date
            valid_date = datetime.strptime(date_input, "%d-%m-%Y")
            # Parse DD-MM-YYYY to YYYY-MM-DD for state
            formatted_date = valid_date.strftime("%Y-%m-%d")
            break
        except ValueError:
            console.print("[bold red]Invalid date or format![/bold red] Please use the exact DD-MM-YYYY format with a valid calendar date (e.g., 14-10-2026).")

    # 4. Step 3: Risk Profile Box
    console.print(
        Panel(
            "Select your preferred risk profile to dictate the trader agent's execution strategy.", 
            title="[bold]Step 3: Risk Profile[/bold]", 
            title_align="left", 
            border_style="blue"
        )
    )
    risk_profile = questionary.select(
        "Select risk profile:",
        choices=["conservative", "neutral", "aggressive"]
    ).ask()

    console.print(f"\n[bold green]Initializing Senzo workflow for {ticker} | {formatted_date} | {risk_profile.capitalize()} profile[/bold green]\n")

    state = {
        "ticker": ticker,
        "date": formatted_date,
        "benchmark": "SPY",
        "risk_profile": risk_profile
    }

    # Tracking Agent Statuses
    agents_status = {
        "Fundamental": "[dim yellow]pending[/dim yellow]",
        "Sentiment": "[dim yellow]pending[/dim yellow]",
        "News": "[dim yellow]pending[/dim yellow]",
        "Technical": "[dim yellow]pending[/dim yellow]",
        "Debate": "[dim yellow]pending[/dim yellow]",
        "Research": "[dim yellow]pending[/dim yellow]",
        "Trader": "[dim yellow]pending[/dim yellow]",
        "Portfolio": "[dim yellow]pending[/dim yellow]"
    }

    # Reusable loading spinner for the table
    in_progress_spinner = Spinner("dots", text="in progress", style="cyan")

    def generate_progress_table():
        table = Table(expand=True, box=None)
        table.add_column("Team", style="cyan", no_wrap=True)
        table.add_column("Agent", style="magenta", no_wrap=True)
        table.add_column("Status", justify="right")

        table.add_row("Analyst Team", "Fundamental Analyst", agents_status["Fundamental"])
        table.add_row("", "Sentiment Analyst", agents_status["Sentiment"])
        table.add_row("", "News Analyst", agents_status["News"])
        table.add_row("", "Technical Analyst", agents_status["Technical"])
        table.add_row("", "", "")
        table.add_row("Research Team", "Bullish and Bearish Debate", agents_status["Debate"])
        table.add_row("", "Research Manager", agents_status["Research"])
        table.add_row("", "", "")
        table.add_row("Trading Team", "Trader (Risk Adjusted)", agents_status["Trader"])
        table.add_row("", "", "")
        table.add_row("Portfolio Mgmt", "Portfolio Manager", agents_status["Portfolio"])
        
        return Panel(table, title="[bold]Workflow Progress[/bold]", border_style="cyan")

    # Execute workflow within a full-width Live context
    with Live(generate_progress_table(), refresh_per_second=10, console=console) as live:
        
        # Fundamental Analyst
        agents_status["Fundamental"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.analysts.fundamental_analyst import fundamental_analyst_node
        state.update(run_step(fundamental_analyst_node, state))
        agents_status["Fundamental"] = "[bold green]✓ complete[/bold green]"

        # Sentiment Analyst
        agents_status["Sentiment"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.analysts.sentimental_analyst import sentimental_analyst_node
        state.update(run_step(sentimental_analyst_node, state))
        agents_status["Sentiment"] = "[bold green]✓ complete[/bold green]"

        # News Analyst
        agents_status["News"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.analysts.news_analyst import news_analyst_node
        state.update(run_step(news_analyst_node, state))
        agents_status["News"] = "[bold green]✓ complete[/bold green]"

        # Technical Analyst
        agents_status["Technical"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.analysts.technical_analyst import technical_analyst_node
        state.update(run_step(technical_analyst_node, state))
        agents_status["Technical"] = "[bold green]✓ complete[/bold green]"

        # Research Debate
        agents_status["Debate"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.researchers.research_debate import research_debate_node
        state.update(run_step(research_debate_node, state))
        agents_status["Debate"] = "[bold green]✓ complete[/bold green]"

        # Research Manager
        agents_status["Research"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.manager.research_manager import research_manager_node
        state.update(run_step(research_manager_node, state))
        agents_status["Research"] = "[bold green]✓ complete[/bold green]"

        # Trader
        agents_status["Trader"] = in_progress_spinner
        live.update(generate_progress_table())
        if risk_profile == "conservative":
            from agents.trader.trader import conservative_trader_node
            state.update(run_step(conservative_trader_node, state))
        elif risk_profile == "aggressive":
            from agents.trader.trader import aggressive_trader_node
            state.update(run_step(aggressive_trader_node, state))
        else:
            from agents.trader.trader import neutral_trader_node
            state.update(run_step(neutral_trader_node, state))
        agents_status["Trader"] = "[bold green]✓ complete[/bold green]"

        # Portfolio Manager
        agents_status["Portfolio"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.manager.portfolio_manager import portfolio_manager_node
        state.update(run_step(portfolio_manager_node, state))
        agents_status["Portfolio"] = "[bold green]✓ complete[/bold green]"
        
        # Final update to show all complete
        live.update(generate_progress_table())

    # After the live progress table is complete, print the reports sequentially
    REPORT_KEYS = {
        "fundamental_report": "Fundamental",
        "sentimental_report": "Sentiment",
        "news_report": "News",
        "technical_report": "Technical",
        "research_verdict": "Research Manager",
        "trader_strategy": "Trader",
        "manager_recc": "Portfolio Manager",
    }
    
    missing = [name for key, name in REPORT_KEYS.items() if bad(state.get(key))]
    
    # Also check debate transcript for safety filters or missing text
    debate = state.get("debate_transcript", [])
    if not debate or any(bad(entry) for entry in debate):
        missing.append("Research Debate")
        
    if missing:
        console.print(Panel(
            f"These reports came back empty, short, or hit safety filters: {', '.join(missing)}.\n"
            "Senzo is currently routing to free models, which can be rate limited or block requests "
            "with safety classifiers. Please run again, or edit the model line in run_task.py "
            "for more reliable results.",
            title="Free model limitation", border_style="yellow"))
    
    console.print("\n")
    console.rule("[bold blue]ANALYST REPORTS[/bold blue]")
    console.print(Panel(Markdown(state.get("fundamental_report") or "No output returned. Try running again."), title="[bold cyan]Fundamental Report[/bold cyan]", border_style="cyan"))
    console.print(Panel(Markdown(state.get("sentimental_report") or "No output returned. Try running again." ), title="[bold magenta]Sentiment Report[/bold magenta]", border_style="magenta"))
    console.print(Panel(Markdown(state.get("news_report") or "No output returned. Try running again."), title="[bold yellow]News Report[/bold yellow]", border_style="yellow"))
    console.print(Panel(Markdown(state.get("technical_report") or "No output returned. Try running again."), title="[bold blue]Technical Report[/bold blue]", border_style="blue"))

    console.rule("[bold blue]RESEARCH DEBATE[/bold blue]")
    for entry in state.get("debate_transcript", []):
        console.print(Panel(entry, border_style="white"))

    console.rule("[bold blue]RESEARCH MANAGER VERDICT[/bold blue]")
    console.print(Panel(Markdown(state.get("research_verdict") or "No output returned. Try running again."), title="[bold green]Research Manager[/bold green]", border_style="green"))

    console.rule("[bold blue]TRADER STRATEGY[/bold blue]")
    console.print(Panel(Markdown(state.get("trader_strategy") or "No output returned. Try running again."), title=f"[bold yellow]{risk_profile.capitalize()} Trader[/bold yellow]", border_style="yellow"))

    console.rule("[bold red]SENZO TRF FINAL RECOMMENDATION[/bold red]")
    console.print(Panel(Markdown(state.get("manager_recc") or "No output returned. Try running again."), title=f"[bold green]Senzo Recommendation — {ticker}[/bold green]", border_style="green"))

if __name__ == "__main__":
    main()