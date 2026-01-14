from google.adk.agents import Agent
from .prompt import VIDEO_ASSEMBLER_PROMPT, VIDEO_ASSEMBLER_DESCRIPTION
from .tools import assemble_video

# Use a fast model for orchestration
MODEL = "gemini-2.0-flash-exp"

video_assembler_agent = Agent(
    name="VideoAssemblerAgent",
    model=MODEL,
    instruction=VIDEO_ASSEMBLER_PROMPT,
    description=VIDEO_ASSEMBLER_DESCRIPTION,
    tools=[assemble_video]
)