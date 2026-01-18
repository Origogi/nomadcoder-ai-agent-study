from google.adk import Agent
from .prompt import SYSTEM_PROMPT

email_refiner = Agent(
    name="email-refiner",
    instructions=SYSTEM_PROMPT,
    model="gemini-2.0-flash-exp",
)
