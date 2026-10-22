from rich.console import Console, Group
from rich.panel import Panel
from rich.markdown import Markdown
from rich.align import Align
from rich.live import Live
from rich.table import Table
from rich.spinner import Spinner
import questionary

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

def main():
    # 1. Main Header Panel with centered Group elements
    header_group = Group(
        Align.center(f"[bold blue]{ascii_logo}[/bold blue]"),
        Align.center("[bold green]Senzo TRF: a multi-agentic research framework for trading.[/bold green]\n"),
        Align.center("[bold][underline]Workflow Steps:[/bold][/underline]\n"),
        Align.center("[italic]Analyst team (fundamentals, sentiment, news, and technical) ➔  Bullish and Bearish researcher debate ➔  Research manager ➔  Trader (risk-adjusted) ➔  Portfolio manager[/italic]\n\n"),
        Align.center("[dim]Built by Aadhi Senthilkumar (github.com/asenszn12) and Sean Enzo Nebres (github.com/sean-25)[/dim]\n")
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
            "Enter the ticker symbol you want to analyze.\n[dim]Example: AAPL, TSLA, SPY[/dim]", 
            title="[bold]Step 1: Ticker Symbol[/bold]", 
            title_align="left", 
            border_style="blue"
        )
    )
    ticker = console.input("[bold cyan]> [/bold cyan]").strip().upper()

    # 3. Step 2: Date Box
    console.print(
        Panel(
            "Set the analysis date you want to get information from (DD-MM-YYYY).", 
            title="[bold]Step 2: Analysis Date[/bold]", 
            title_align="left", 
            border_style="blue"
        )
    )
    date_input = console.input("[bold cyan]> [/bold cyan]").strip()
    
    # Parse DD-MM-YYYY to YYYY-MM-DD for state
    try:
        parts = date_input.split("-")
        formatted_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
    except IndexError:
        formatted_date = date_input 

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
        state.update(fundamental_analyst_node(state))
        agents_status["Fundamental"] = "[bold green]✓ complete[/bold green]"

        # Sentiment Analyst
        agents_status["Sentiment"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.analysts.sentimental_analyst import sentimental_analyst_node
        state.update(sentimental_analyst_node(state))
        agents_status["Sentiment"] = "[bold green]✓ complete[/bold green]"

        # News Analyst
        agents_status["News"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.analysts.news_analyst import news_analyst_node
        state.update(news_analyst_node(state))
        agents_status["News"] = "[bold green]✓ complete[/bold green]"

        # Technical Analyst
        agents_status["Technical"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.analysts.technical_analyst import technical_analyst_node
        state.update(technical_analyst_node(state))
        agents_status["Technical"] = "[bold green]✓ complete[/bold green]"

        # Research Debate
        agents_status["Debate"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.researchers.research_debate import research_debate_node
        state.update(research_debate_node(state))
        agents_status["Debate"] = "[bold green]✓ complete[/bold green]"

        # Research Manager
        agents_status["Research"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.manager.research_manager import research_manager_node
        state.update(research_manager_node(state))
        agents_status["Research"] = "[bold green]✓ complete[/bold green]"

        # Trader
        agents_status["Trader"] = in_progress_spinner
        live.update(generate_progress_table())
        if risk_profile == "conservative":
            from agents.trader.trader import conservative_trader_node
            state.update(conservative_trader_node(state))
        elif risk_profile == "aggressive":
            from agents.trader.trader import aggressive_trader_node
            state.update(aggressive_trader_node(state))
        else:
            from agents.trader.trader import neutral_trader_node
            state.update(neutral_trader_node(state))
        agents_status["Trader"] = "[bold green]✓ complete[/bold green]"

        # Portfolio Manager
        agents_status["Portfolio"] = in_progress_spinner
        live.update(generate_progress_table())
        from agents.manager.portfolio_manager import portfolio_manager_node
        state.update(portfolio_manager_node(state))
        agents_status["Portfolio"] = "[bold green]✓ complete[/bold green]"
        
        # Final update to show all complete
        live.update(generate_progress_table())

    # After the live progress table is complete, print the reports sequentially
    console.print("\n")
    console.rule("[bold blue]ANALYST REPORTS[/bold blue]")
    console.print(Panel(Markdown(state.get("fundamental_report", "")), title="[bold cyan]Fundamental Report[/bold cyan]", border_style="cyan"))
    console.print(Panel(Markdown(state.get("sentimental_report", "")), title="[bold magenta]Sentiment Report[/bold magenta]", border_style="magenta"))
    console.print(Panel(Markdown(state.get("news_report", "")), title="[bold yellow]News Report[/bold yellow]", border_style="yellow"))
    console.print(Panel(Markdown(state.get("technical_report", "")), title="[bold blue]Technical Report[/bold blue]", border_style="blue"))

    console.rule("[bold blue]RESEARCH DEBATE[/bold blue]")
    for entry in state.get("debate_transcript", []):
        console.print(Panel(entry, border_style="white"))

    console.rule("[bold blue]RESEARCH MANAGER VERDICT[/bold blue]")
    console.print(Panel(Markdown(state.get("research_verdict", "")), title="[bold green]Research Manager[/bold green]", border_style="green"))

    console.rule("[bold blue]TRADER STRATEGY[/bold blue]")
    console.print(Panel(Markdown(state.get("trader_strategy", "")), title=f"[bold yellow]{risk_profile.capitalize()} Trader[/bold yellow]", border_style="yellow"))

    console.rule("[bold red]SENZO TRF FINAL RECOMMENDATION[/bold red]")
    console.print(Panel(Markdown(state.get("manager_recc", "")), title=f"[bold green]Senzo Recommendation — {ticker}[/bold green]", border_style="green"))

if __name__ == "__main__":
    main()