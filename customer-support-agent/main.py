import asyncio

import dotenv
import streamlit as st
from openai import OpenAI

from agents import (
    RunContextWrapper,
    Runner,
    SQLiteSession,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered
)
from models import UserAccountContext
from my_agents.triage_agent import triage_agent

dotenv.load_dotenv()


user_account_ctx = UserAccountContext(
    customer_id=1,
    name="Origogi",
    email="email@email.com",
    tier="basic",
)

client = OpenAI()

if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-history",
        "customer-support-memory.db",
    )

if "agent" not in st.session_state:
    st.session_state["agent"] = triage_agent

session = st.session_state["session"]


async def paint_history():
    messages = await session.get_items()
    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.write(message["content"])
                else:
                    if message["type"] == "message":
                        st.write(message["content"][0]["text"].replace("$", "\$"))


asyncio.run(paint_history())


async def run_agent(message):
    with st.chat_message("ai"):
        text_placeholder = st.empty()
        response = ""

        try:
            run_agent = st.session_state["agent"]

            stream = Runner.run_streamed(
                run_agent,
                message,
                session=session,
                context=user_account_ctx,
            )

            async for event in stream.stream_events():
                if event.type == "raw_response_event":
                    if event.data.type == "response.output_text.delta":
                        response += event.data.delta
                        text_placeholder.write(response.replace("$", "\$"))
                elif event.type == "agent_updated_stream_event":
                    from_agent = st.session_state["agent"]
                    to_agent = event.new_agent

                    if from_agent.name != to_agent.name:
                        st.write(
                            f"🤖 Transfered from {from_agent.name} to {to_agent.name}"
                        )
                        st.session_state["agent"] = to_agent

                        text_placeholder = st.empty()
                        response = ""

        except InputGuardrailTripwireTriggered:
            st.write("I can't help you with that.")
        except OutputGuardrailTripwireTriggered:
            st.write("Can show you that answer.")
            st.session_state["text_placeholder"].empty()


message = st.chat_input(
    "Write a message for your assistant",
)

if message:
    with st.chat_message("human"):
        st.write(message)
    asyncio.run(run_agent(message))


with st.sidebar:
    reset = st.button("Reset memory")
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(session.get_items()))
