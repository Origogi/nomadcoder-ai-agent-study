from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.tool_context import ToolContext
from .prompt import PROMPT
from .sub_agents.data_analyst import data_analyst
from .sub_agents.finance_analyst import financial_analyst
from .sub_agents.news_analyst import news_analyst

MODEL = "gemini-2.5-flash"


def save_advice_report(tool_context : ToolContext, summary :str):
    state = tool_context.state

    data_analyst_result = state.get("data_analyst_result")
    finance_analyst_result = state.get("finance_analyst_result")
    news_analyst_result = state.get("news_analyst_result")

    report = f"""
    # Exetuve Summary and advice:
    {summary}

    ## Data Analyst Report:
    {data_analyst_result}

    ## Financial Analyst Report:
    {finance_analyst_result}

    ## News Analyst Report:
    {news_analyst_result}

    """
    state["report"] = report
    return {
        "success" : True
    }


financial_advisor = Agent(
    name="FinancialAdvisor",
    instruction=PROMPT,
    model=MODEL,
    tools=[
        AgentTool(agent=financial_analyst),
        AgentTool(agent=data_analyst),
        AgentTool(agent=news_analyst),
        save_advice_report,
    ],
)


root_agent = financial_advisor
