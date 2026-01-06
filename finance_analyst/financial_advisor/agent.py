from google.adk.agents import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

MODEL="gemini-2.5-flash"

def get_weather(city: str):
    return f"The Weather in {city} is 40 degrees."

def convert_units(degrees:int):
    return f"That is 40 farenheit"

geo_agent = Agent(
    name="GeoAgent",
    instruction="You help with geo question",
    description="Transfer to this agent when you have a geo related question.",
    model=MODEL,
)

weather_agent = Agent(
    name="WeatherAgent",
    instruction="You help the user with weather related questions",
    model=MODEL,
    tools=[
        # GoogleSearchTool(bypass_multi_tools_limit=True),
        get_weather,
        convert_units
    ],
    sub_agents=[
        geo_agent
    ]
)

root_agent = weather_agent
