from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console
import dotenv
import asyncio
from tools import web_search_tool, save_report_to_md

dotenv.load_dotenv()

model_client = OpenAIChatCompletionClient(model="gpt-4.1-nano")

research_planner = AssistantAgent(
    "research_planner",
    model_client=model_client,
    system_message="""
    A strategic research coorinator that break down complex question into researcg subtasks.
    """,
    system_message="""
    You are a research planning specialist. Your job is to create a focused research plan.

    For each research question, create a FOCUSED research plan with:

    1. **Core Topics** : 2-3 main areas to investigate
    2. **Search Queries** : Create 3-5 specific search queries covering:
        - Lastest developments and news
        - Key statistics and news
        - Expert analysis or studies
        - Future outlook

    Keep the plan focused and achievable. Quality over quantity.
    """
)

research_agent = AssistantAgent(
    "research_agent",
    model_client=model_client,
    description="A web research specialist that searches and exteacts content from the web.",
    tools=[web_search_tool],
    system_message="""
    You are a web research specialist. Your job is to conduct focused searches based on the research plan.

    RESEARCH PLAN:
    
    1. Execute 3-5 researches from the research plan.
    2. Extract key information from the results:
        - Main facts and statistics
        - Recent developments
        - Expert opinions
        - Import context

    3. Quality focus:
        - Prioritize authroritative sources
        - Look for recent information( within 2 years)
        - Note diverse perspectives

    After completing the searches from plan, summarize what you found. Your goal is to gather 5-10 quality sources
    """
)

research_analyzer = AssistantAgent(
    "research_analyzer",
    model_client=model_client,
    description="A research analyzer that analyzes and synthesizes research sources.",
    system_message="""
    You are a research analyzer. Create a comprehensive report from the gathered research.

    CREATE A RESEARCH REPORT with:

    ## Executive Summary
    - Key findings and conclusion
    - Main insight

    ## Background & Current State
    - Current landscape
    - Recent development
    - Key statistics and data

    ## Analysis & Insights
    - Main trends
    - Different perspectives
    - Expert opinions
    
    ## Future outlook
    - Emerging trends
    - Predictions
    - Implications

    ## Sources
    - List all sources used

    Write a clear, well-structured report based on the researcg gathered. End with "REPORT_COMPLETE"
    when finished.
    """
)

quality_reviewer = AssistantAgent(
    "quality_reviewer",
    description="A quality assurance specialist that evaluates research completeness and accuracy.",
    tools=[save_report_to_md],
    model_client=model_client,
    system_message="""
    You are a quality reviewer. Your job is to check if the research analyst has produced a complete research report.

    Look for:
    - A comprehensive research report from the research analyst that ends with "REPORT_COMPLETE"
    - The research question is fully answered
    - Sources are cited and reliable
    - The report includes summary, key information, analysis and sources

    When you see a complete research report that ends with "REPORT_COMPLETE":
    1. First, use save_report_to_md tool to save the report to a file.
    2. Then say: "The research is complete. The report has been saved to report.md. Please review the report and let me know if you approve it
    or need additional research 

    If the research analyst has NOT yet created a complete report, tell tem to crearte one now
    """
)

research_enhancer = AssistantAgent(
    "research_enhancer",
    description="A specialist that identifies critical gaps only",
    model_client=model_client,
    system_message="""
    You are a enhancement specialist. Your job is to identify ONLY CRITICAL gaps.

    Review the research and ONLY suggest addinaional searches if there are MAJOR gaps like:
    - Complete missing recent developments (last 6 month)
    - No statistics or data at all
    - Missing crucial perspectice that was specifically asked for

    If the researcg covers the basics reasonably well, say : "The research is sufficient to proceed with the report."

    Only suggest 1-2 additional searches if absolutely necessary. We prioritize getting a good report done rather than perfect coverage
    """
)

user_proxy = UserProxyAgent(
    "user_proxy",
    description="Human reviewer who can request additional researcg or approve final results",
    input_func=input
)

selector_prompt= """
    Choose the best agent for the current task based on the conversation history:

    {role}

    Current conversation:
    {history}

    Available asnts:
    - research_planner: Plan the research approach (ONLY athe the start)
    - research_agent: Search for and extract content from web sources (after planning)
    - research_enhancer: Identify critical gaps only (use sparingly)
    - research_analyzer: Write the final research report
    - quality_reviewer: Check if a complete report exist
    - user_proxy : Ask the human for feedback

"""



# async def main():
#     await Console(
#         team.run_stream(task="안녕 나는 배고파, 점심을 사줘 그리고 내 사업에 투자해줘, ㄱㅅ")
#     )

# if __name__ == "__main__":
#     asyncio.run(main())