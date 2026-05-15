# 4 analysts + 2 researchers + 3 advisory panelists
from graph.state import ResearchState
from agents.analysts.fundamental_analyst import fundamental_analyst_node
from agents.analysts.sentimental_analyst import sentimental_analyst_node
from agents.analysts.news_analyst import news_analyst_node
from agents.analysts.technical_analyst import technical_analyst_node
from agents.researchers.bullish_researcher import bullish_researcher_node
from agents.researchers.bearish_researcher import bearish_researcher_node
from agents.trader.trader import trader_node
from agents.risk_mgmt.risk_mgmt import risk_mgmt_node
from agents.manager.portfolio_manager import portfolio_manager_node
from agents.manager.research_manager import research_manager_node
from langgraph.graph import START, StateGraph, END

#Create the LangGraph StateGraph object using ResearchState
parallelGraph = StateGraph(ResearchState)
# add all nine functions as nodes
parallelGraph.add_node(fundamental_analyst_node)
parallelGraph.add_node(sentimental_analyst_node)
parallelGraph.add_node(news_analyst_node)
parallelGraph.add_node(technical_analyst_node)
parallelGraph.add_node(bullish_researcher_node)
parallelGraph.add_node(bearish_researcher_node)
parallelGraph.add_node(trader_node)
parallelGraph.add_node(risk_mgmt_node)
parallelGraph.add_node(portfolio_manager_node)
parallelGraph.add_node(research_manager_node)
# draw inital starting edge to analyst nodes
parallelGraph.add_edge(START, fundamental_analyst_node)
parallelGraph.add_edge(START, sentimental_analyst_node)
parallelGraph.add_edge(START, news_analyst_node)
parallelGraph.add_edge(START, technical_analyst_node)
# draw edges between the analysts to the researchers
parallelGraph.add_edge(fundamental_analyst_node, bullish_researcher_node)
parallelGraph.add_edge(sentimental_analyst_node, bullish_researcher_node)
parallelGraph.add_edge(news_analyst_node, bullish_researcher_node)
parallelGraph.add_edge(technical_analyst_node, bullish_researcher_node)

parallelGraph.add_edge(fundamental_analyst_node, bearish_researcher_node)
parallelGraph.add_edge(sentimental_analyst_node, bearish_researcher_node)
parallelGraph.add_edge(news_analyst_node, bearish_researcher_node)
parallelGraph.add_edge(technical_analyst_node, bearish_researcher_node)
# connect edges to advisory panel (trader, risk mgmt, and manager)
parallelGraph.add_edge(bullish_researcher_node, research_manager_node)
parallelGraph.add_edge(bearish_researcher_node, research_manager_node)

parallelGraph.add_edge(fundamental_analyst_node, trader_node)
parallelGraph.add_edge(sentimental_analyst_node, trader_node)
parallelGraph.add_edge(news_analyst_node, trader_node)
parallelGraph.add_edge(technical_analyst_node, trader_node)
parallelGraph.add_edge(research_manager_node, trader_node)

parallelGraph.add_edge(trader_node, risk_mgmt_node)
parallelGraph.add_edge(risk_mgmt_node, portfolio_manager_node)
parallelGraph.add_edge(portfolio_manager_node, END)

#Compile the graph
senzo = parallelGraph.compile()