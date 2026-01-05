from google.adk.agents import Agent

weather_agent = Agent(
    name="WeatherAgent",
    instruction="You help the user with weather related questions",
    model="gemini-2.0-flash"
)

root_agent = weather_agent