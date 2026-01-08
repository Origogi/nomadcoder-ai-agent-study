from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .prompt import PROMPT
from .sub_agents.data_analyst import data_analyst
from .sub_agents.finance_analyst import financial_analyst
from .sub_agents.news_analyst import news_analyst

MODEL = "gemini-2.5-flash"


def save_advice_report():
    pass


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
