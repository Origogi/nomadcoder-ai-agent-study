from typing import Literal, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

checkpointer = MemorySaver()


load_dotenv()


llm = init_chat_model("openai:gpt-4o-mini")


class EmailState(TypedDict):
    email: str
    category: Literal['spam', 'normal', 'urgent']
    priority_score: int
    response : str

class EmailClassificationOutput(BaseModel):
    category : Literal['spam', 'normal', 'urgent'] = Field(description="The category of the email based on its content.")

class PriorityScoreOutput(BaseModel):
    priority_score : int = Field(description="The priority score from 1 to 10, where 10 is the highest priority.", ge = 1, le = 10)


def categorize_email(state : EmailState):
    s_llm = llm.with_structured_output(EmailClassificationOutput)

    response = s_llm.invoke(
        f"""
        Classify this eamil into one of three categories:

        - urgent : The email requires immediate attention and action.
        - normal : The email is important but does not require immediate action.
        - spam : Promotional, marketing, or irrelevant emails that do not require a response.

        Email: {state['email']}
        """
    )
    
    return {
        "category": response.category
    }


def assign_priority(state : EmailState):
    s_llm = llm.with_structured_output(PriorityScoreOutput)

    response = s_llm.invoke(
        f"""
        Assign a priority score from 1 to 10 based on the email category, where 10 is the highest priority.
        - urgent : 8-10
        - normal : 4-7
        - spam : 1-3

        Email category: {state['category']}
        """
    )

    return {
        "priority_score": response.priority_score
    }


def draft_response(state : EmailState):
    response = llm.invoke(
        f"""
        Draft a brief, professional response for this {state['category']} email. 
        
        Original email content: {state['email']}
        Category: {state['category']}
        Priority score: {state['priority_score']} / 10

        Guidelines:
        _ Urgent : Acknowledge receipt, express understanding of urgency, and indicate next steps or expected response time.
        _ Normal : Acknowledge receipt, express appreciation for the email, and indicate that you will review and respond in a timely manner.
        _ Spam : Politely decline or ignore the email, indicating that it has been categorized as spam and will not be addressed.

        Keep response under 2 sentences.
        """
    )

    return {
        "response": response.content
    }



graph_builder = StateGraph(EmailState)

graph_builder.add_node("categorize_email", categorize_email)
graph_builder.add_node("assign_priority", assign_priority)
graph_builder.add_node("draft_response", draft_response)

graph_builder.add_edge(START, "categorize_email")
graph_builder.add_edge("categorize_email", "assign_priority")
graph_builder.add_edge("assign_priority", "draft_response")
graph_builder.add_edge("draft_response", END)

graph = graph_builder.compile(checkpointer=checkpointer)

result = graph.invoke(
    {"email": "I have an offer for you"},
    config={"configurable": {"thread_id": "1"}}
)
print(result)