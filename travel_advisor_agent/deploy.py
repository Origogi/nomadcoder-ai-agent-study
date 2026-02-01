import vertexai
from vertexai import agent_engines
from travel_advisor.agent import travel_advisor_agent
from vertexai.preview import reasoning_engines
import dotenv
import os

dotenv.load_dotenv()

PROJECT_ID = "gen-lang-client-0614714161"
LOCATION = "us-central1"
BUCKET = "gs://origogi-weather-agent"

vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=BUCKET)

app = reasoning_engines.AdkApp(agent=travel_advisor_agent, enable_tracing=True)

remote_app = agent_engines.create(
    display_name="Travel Advisor Agent",
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent-engines]",
        "google-adk>=0.1.0",
        "google-genai>=0.2.0",
        "pydantic>=2.0",
    ],
    extra_packages=["travel_advisor"],
    env_vars={"GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY")},
)

print(f"Deployment successful. Resource name: {remote_app.resource_name}")
