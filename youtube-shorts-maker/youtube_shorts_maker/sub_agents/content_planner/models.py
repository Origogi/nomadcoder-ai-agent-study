from pydantic import BaseModel, Field
from typing import List


class SceneOutput(BaseModel):
    id : int = Field(description="Scene ID Number")
    narration : str = Field(description="What the narrator of this scene should say")
    visual_description : str = Field(description="Detailed description for image generation")
    embedded_text : str = Field(description="Text overlay for the image")
    embedded_text_location : str = Field(description="Whare to position the text on the image (i.e 'top_center' or 'bottom_left')")
    duration : int = Field(description="Duration in seconds for this scene")

class ContentPlanOutput(BaseModel):
    topic : str = Field(description="The topic of the Youtube Short")
    total_duration : str = Field(description="Total video duration in seconds (max 20)")
    scenes: List[SceneOutput] = Field(
        description="List of scens (agent decies how many)"
    )