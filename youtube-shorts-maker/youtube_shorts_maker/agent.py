from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.content_planner.agent import content_planner_agent
from .sub_agents.asset_generator.agent import asset_generator_agent
from .sub_agents.video_assembler.agent import video_assembler_agent
from .prompt import SHORTS_PRODUCER_DESCRIPTION, SHORTS_PRODUCER_PROMPT
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

MODEL = "gemini-3-pro-preview"


def before_model_callback(callback_context : CallbackContext):
    # 현재 세션에서 마지막 메시지를 가져오고 싶어, 가드레일을 만들거야
    
    return None



shorts_producer_agent = Agent(
    name="ShortsProducerAgent",
    model=MODEL,
    description=SHORTS_PRODUCER_DESCRIPTION,
    instruction=SHORTS_PRODUCER_PROMPT,
    tools=[
        AgentTool(agent=content_planner_agent),
        AgentTool(agent=asset_generator_agent),
        AgentTool(agent=video_assembler_agent),
    ],
    before_agent_callback=before_model_callback,
)

root_agent = shorts_producer_agent
