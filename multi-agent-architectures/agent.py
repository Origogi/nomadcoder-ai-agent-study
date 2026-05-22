from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

MODEL = "openai:gpt-4o-mini"

history_agent = create_react_agent(
    model = MODEL,
    tools = [],
    name="history_agent",
    prompt= "You are a history expert. You only answer questions about history."
)

geography_agent = create_react_agent(
    model = MODEL,
    tools = [],
    name="geography_agent",
    prompt= "You are a geography expert. You only answer questions about geography."
)

maths_agent = create_react_agent(
    model = MODEL,
    tools = [],
    name="maths_agent",
    prompt= "You are a maths expert. You only answer questions about maths."
)

philosophy_agent = create_react_agent(
    model = MODEL,
    tools = [],
    name="philosophy_agent",
    prompt= "You are a philosophy expert. You only answer questions about philosophy."
)