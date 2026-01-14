
from google.adk.agents import Agent
from .prompt import VOICE_GENERATOR_DESCRIPTION, VOICE_GENERATOR_PROMPT
from .tools import generate_narrations

# Orchestrator model can be gemini-2.0-flash-exp 
# to decide which voice to use, while the tool uses the specific TTS model.
MODEL = "gemini-2.0-flash-exp"

voice_generator_agent = Agent(
    name="VoiceGeneratorAgent",
    instruction=VOICE_GENERATOR_PROMPT,
    description=VOICE_GENERATOR_DESCRIPTION,
    model=MODEL,
    tools=[
        generate_narrations
    ]
)