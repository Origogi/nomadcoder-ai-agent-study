from google.adk.agents import Agent
from .prompt import SHORTS_PRODUCER_DESCRIPTION, SHORTS_PRODUCER_PROMPT
from .models import ContentPlanOutput

MODEL = "gemini-3-pro-preview"

content_planner_agent = Agent(
    name="ContentPlannerAgent",
    description=SHORTS_PRODUCER_DESCRIPTION,
    instruction=SHORTS_PRODUCER_PROMPT,
    model=MODEL,
    output_schema=ContentPlanOutput
)