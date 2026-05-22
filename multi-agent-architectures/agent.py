from typing import NotRequired, Literal

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition, InjectedState
from langgraph.types import Command
from pydantic import BaseModel
from typing_extensions import Annotated


class SupervisorOutput(BaseModel):
    next_agent: Literal["korean_agent", "greek_agent", "spanish_agent", "__end__"]
    reasoning: str


load_dotenv()


class AgentState(MessagesState):
    current_agent: NotRequired[str]
    transfered_by: NotRequired[str]
    reasoning: NotRequired[str]


llm = init_chat_model("openai:gpt-5-mini-2025-08-07")


def make_agent_tool(tool_name, tool_description, system_prompt, tools):
    def agent_node(state: AgentState):
        llm_with_tools = llm.bind_tools(tools)
        response = llm_with_tools.invoke(
            f"""
        {system_prompt}


        Conversation history:
        {state["messages"]}
        """
        )
        return {"messages": [response]}

    agent_builder = StateGraph(AgentState)
    agent_builder.add_node("agent", agent_node)
    agent_builder.add_node("tools", ToolNode(tools))
    agent_builder.add_edge(START, "agent")
    agent_builder.add_conditional_edges("agent", tools_condition)
    agent_builder.add_edge("tools", "agent")
    agent_builder.add_edge("agent", END)

    agent = agent_builder.compile()

    @tool(
        name_or_callable=tool_name,
        description=tool_description,
    )
    def agent_tool(state: Annotated[dict, InjectedState]):
        result = agent.invoke(state)

        return result["messages"][-1].content

    return agent_tool


def supervisor(state: AgentState):
    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response],
    }

tools = [
    make_agent_tool(
        "korean_agent",
        "An agent that is fluent in Korean. Use this tool to handle conversations in Korean.",
        "You are a helpful assistant that is fluent in Korean. You can assist with any questions or tasks that require understanding of the Korean language.",
        [],
    ),
    make_agent_tool(
        "greek_agent",
        "An agent that is fluent in Greek. Use this tool to handle conversations in Greek.",
        "You are a helpful assistant that is fluent in Greek. You can assist with any questions or tasks that require understanding of the Greek language.",
        [],
    ),
    make_agent_tool(
        "spanish_agent",
        "An agent that is fluent in Spanish. Use this tool to handle conversations in Spanish.",
        "You are a helpful assistant that is fluent in Spanish. You can assist with any questions or tasks that require understanding of the Spanish language.",
        [],
    ),
]

graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "supervisor",
    supervisor,
)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START, "supervisor")
graph_builder.add_conditional_edges("supervisor", tools_condition)
graph_builder.add_edge("tools", "supervisor")
graph_builder.add_edge("supervisor", END)

graph = graph_builder.compile()
