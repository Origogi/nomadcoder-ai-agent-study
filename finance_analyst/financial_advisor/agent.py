from google.adk.agents import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool


def get_weather(city: str):
    return f"The Weather in {city} is 40 degrees."

def convert_units(degrees:int):
    return f"That is 40 farenheit"


weather_agent = Agent(
    name="WeatherAgent",
    instruction="You help the user with weather related questions",
    model="gemini-2.0-flash",
    tools=[
        # GoogleSearchTool(),
        get_weather,
        convert_units
    ],
)

root_agent = weather_agent
