from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
import questionary

console = Console()

ascii_logo = r"""
 _____/\\\\\\\\\_____________________________________________________________/\\\\\\\\\\\\\\\____/\\\\\\\\\______/\\\\\\\\\\\\\\\_        
___/\\\/////////\\\__________________________________________________________\///////\\\/////___/\\\///////\\\___\/\\\///////////__       
__\//\\\______\///_________________________________________________________________\/\\\_______\/\\\_____\/\\\___\/\\\_____________      
___\////\\\____________/\\\\\\\\___/\\/\\\\\\____/\\\\\\\\\\\_____/\\\\\__________\/\\\_______\/\\\\\\\\\\\/____\/\\\\\\\\\\\_____     
______\////\\\________/\\\/////\\\_\/\\\////\\\__\///////\\\/____/\\\///\\\________\/\\\_______\/\\\//////\\\____\/\\\///////______    
_________\////\\\____/\\\\\\\\\\\__\/\\\__\//\\\______/\\\/_____/\\\__\//\\\_______\/\\\_______\/\\\____\//\\\___\/\\\_____________   
__/\\\______\//\\\__\//\\///////___\/\\\___\/\\\____/\\\/______\//\\\__/\\\________\/\\\_______\/\\\_____\//\\\__\/\\\_____________  
_\///\\\\\\\\\\\/____\//\\\\\\\\\\_\/\\\___\/\\\__/\\\\\\\\\\\__\///\\\\\/_________\/\\\_______\/\\\______\//\\\_\/\\\_____________ 
___\///////////_______\//////////__\///____\///__\///////////_____\/////___________\///________\///________\///__\///____________
"""

def main():
    console.print(ascii_logo, style="bold blue")

    ticker = console.input("[bold]Enter ticker:[/bold] ").upper()
    date = console.input("[bold]Enter date (DD-MM-YYYY):[/bold] ")

    # parse DD-MM-YYYY to YYYY-MM-DD for state
    parts = date.split("-")
    formatted_date = f"{parts[2]}-{parts[1]}-{parts[0]}"

    risk_profile = questionary.select(
        "Select risk profile:",
        choices=["conservative", "neutral", "aggressive"]
    ).ask()

    console.print(f"\n[bold green]Running Senzo for {ticker} | {formatted_date} | {risk_profile.capitalize()} profile[/bold green]\n")

    state = {
        "ticker": ticker,
        "date": formatted_date,
        "benchmark": "SPY",
        "risk_profile": risk_profile
    }

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:

        task = progress.add_task("Running Fundamental Analyst...", total=None)
        from agents.analysts.fundamental_analyst import fundamental_analyst_node
        state.update(fundamental_analyst_node(state))
        progress.update(task, description="[green]✓ Fundamental Analyst complete")

        task = progress.add_task("Running Sentiment Analyst...", total=None)
        from agents.analysts.sentimental_analyst import sentimental_analyst_node
        state.update(sentimental_analyst_node(state))
        progress.update(task, description="[green]✓ Sentiment Analyst complete")

        task = progress.add_task("Running News Analyst...", total=None)
        from agents.analysts.news_analyst import news_analyst_node
        state.update(news_analyst_node(state))
        progress.update(task, description="[green]✓ News Analyst complete")

        task = progress.add_task("Running Technical Analyst...", total=None)
        from agents.analysts.technical_analyst import technical_analyst_node
        state.update(technical_analyst_node(state))
        progress.update(task, description="[green]✓ Technical Analyst complete")

        task = progress.add_task("Running Research Debate...", total=None)
        from agents.researchers.research_debate import research_debate_node
        state.update(research_debate_node(state))
        progress.update(task, description="[green]✓ Research Debate complete")

        task = progress.add_task("Running Research Manager...", total=None)
        from agents.manager.research_manager import research_manager_node
        state.update(research_manager_node(state))
        progress.update(task, description="[green]✓ Research Manager complete")

        task = progress.add_task("Running Trader...", total=None)
        if risk_profile == "conservative":
            from agents.trader.trader import conservative_trader_node
            state.update(conservative_trader_node(state))
        elif risk_profile == "aggressive":
            from agents.trader.trader import aggressive_trader_node
            state.update(aggressive_trader_node(state))
        else:
            from agents.trader.trader import neutral_trader_node
            state.update(neutral_trader_node(state))
        progress.update(task, description="[green]✓ Trader complete")

        task = progress.add_task("Running Portfolio Manager...", total=None)
        from agents.manager.portfolio_manager import portfolio_manager_node
        state.update(portfolio_manager_node(state))
        progress.update(task, description="[green]✓ Portfolio Manager complete")

    console.rule("[bold blue]ANALYST REPORTS")
    console.print(Panel(Markdown(state["fundamental_report"]), title="[bold cyan]Fundamental Report[/bold cyan]", style="cyan"))
    console.print(Panel(Markdown(state["sentimental_report"]), title="[bold magenta]Sentiment Report[/bold magenta]", style="magenta"))
    console.print(Panel(Markdown(state["news_report"]), title="[bold yellow]News Report[/bold yellow]", style="yellow"))
    console.print(Panel(Markdown(state["technical_report"]), title="[bold blue]Technical Report[/bold blue]", style="blue"))

    console.rule("[bold blue]RESEARCH DEBATE")
    for entry in state["debate_transcript"]:
        console.print(Panel(entry, style="white"))

    console.rule("[bold blue]RESEARCH MANAGER VERDICT")
    console.print(Panel(Markdown(state["research_verdict"]), title="[bold green]Research Manager[/bold green]", style="green"))

    console.rule("[bold blue]TRADER STRATEGY")
    console.print(Panel(Markdown(state["trader_strategy"]), title=f"[bold yellow]{risk_profile.capitalize()} Trader[/bold yellow]", style="yellow"))

    console.rule("[bold red]FINAL RECOMMENDATION")
    console.print(Panel(Markdown(state["manager_recc"]), title=f"[bold green]Senzo Recommendation — {ticker}[/bold green]", style="green"))

if __name__ == "__main__":
    main()