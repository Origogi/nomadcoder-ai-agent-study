from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.content_planner.agent import content_planner_agent
from .sub_agents.asset_generator.agent import asset_generator_agent
from .sub_agents.video_assembler.agent import video_assembler_agent
from .prompt import SHORTS_PRODUCER_DESCRIPTION, SHORTS_PRODUCER_PROMPT
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

MODEL = "gemini-3-pro-preview"


def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    last_message = llm_request.contents[-1]

    if last_message and last_message.role == "user" and last_message.parts:
        text = last_message.parts[-1].text or ""

        if "hummus" in text:
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text="죄송합니다. 그것을 도와드릴수 없습니다.",
                        ),
                    ],
                )
            )

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
    before_model_callback=before_model_callback,
)

root_agent = shorts_producer_agent
