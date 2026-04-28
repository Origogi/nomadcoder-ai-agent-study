from typing import Literal, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class EmailState(TypedDict):
    email: str
    category: Literal['spam', 'normal', 'urgent']
    priority_score: int
    response : str


def categorize_email(state : EmailState):
    email = state['email'].lower()

    if "urgent" in email or "asap" in email:
        category = "urgent"
    elif "offer" in email or "discount" in email:
        category = "spam"
    else:        
        category = "normal"

    return {
        "category": category
    }


def assingn_priority(state : EmailState):
    scores = {
        "urgent": 10,
        "normal": 5,
        "spam": 1
    }

    return {
        "priority_score": scores[state['category']]
    }

def draft_response(state : EmailState):
    responses = {
        "urgent": "We have received your email and will get back to you as soon as possible.",
        "normal": "Thank you for your email. We will review it and respond within 24-48 hours.",
        "spam": "Your email has been marked as spam and will not be reviewed."
    }

    return {
        "response": responses[state['category']]
    }



graph_builder = StateGraph(EmailState)

graph_builder.add_node("categorize_email", categorize_email)
graph_builder.add_node("assign_priority", assingn_priority)
graph_builder.add_node("draft_response", draft_response)

graph_builder.add_edge(START, "categorize_email")
graph_builder.add_edge("categorize_email", "assign_priority")
graph_builder.add_edge("assign_priority", "draft_response")
graph_builder.add_edge("draft_response", END)

graph = graph_builder.compile()

result = graph.invoke({
    "email": "I have offer for you"
})

print(result)