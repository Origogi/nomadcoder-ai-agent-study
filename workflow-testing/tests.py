import pytest
from main import graph
import dotenv

dotenv.load_dotenv()

@pytest.mark.parametrize(
    "email, expected_category, min_score, max_score",
    [
        ("this is an urgent email", "urgent", 8, 10),
        ("i wanna talk to you", "normal", 4, 7),
        ("i have an offer for you", "spam", 1, 3),
    ]
)
def test_full_graph(email, expected_category, min_score, max_score):

    result = graph.invoke(
        {
            "email": email
        },
        config={
            "configurable": {
                "thread_id" : "1"
            }
        }
    )

    assert result['category'] == expected_category
    assert min_score <= result['priority_score'] <= max_score

def test_individual_nodes():
    # categorize_email

    result = graph.nodes["categorize_email"].invoke({
        "email" : "check out this offer"
    })

    assert result["category"] == "spam"

    # assign_priority

    result = graph.nodes["assign_priority"].invoke({
        "category" : "spam",
        "email" : "check out this offer"
    })

    assert 1 <= result["priority_score"] <= 3

    # draft_response

    # result = graph.nodes["draft_response"].invoke({
    #     "category" : "spam"
    # })

    # assert result["response"] == "This email has been categorized as spam and will be ignored."

def test_partial_execution():
    # Start -> categorize_email -> assign_priority

    graph.update_state(
        config={
            "configurable": {
                "thread_id" : "1"
            }
        },
        values={
            "email" : "please check out this offer",
            "category" : "spam",
        },
        as_node="categorize_email"
    )

    result = graph.invoke(
        None,
        config={
            "configurable": {
                "thread_id" : "1"
            }
        },
        interrupt_after="draft_response"
    )

    assert result['priority_score'] >= 1 and result['priority_score'] <= 3