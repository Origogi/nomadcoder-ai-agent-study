from google.adk.agents import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool


MODEL="gemini-2.5-flash"


news_analyst = Agent(
    name="NewsAnalyst",
    model=MODEL,
    description="Uses Google Search to find and analyze recent news from the web.",
    instruction="""
    You are a News Analyst Specialist who uses Google Search to find current information. Your job:

    1. **Web Search**: Use google_search() to find recent news about a company.
    2. **Summarize Findings**: Explain what you found and its relevance

    **Your Tool:**
    - **google_search()**: Google Search for company news and market updates

    Search for current news and summarize the findings clearly.
    """,
    output_key="news_analyst_result",
    tools=[
        GoogleSearchTool(),
    ],
)