from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console
import dotenv
import asyncio

dotenv.load_dotenv()

model = OpenAIChatCompletionClient(model="gpt-4.1-nano")

clarity_agent = AssistantAgent(
    "ClarityAgent",
    model_client=model,
    system_message="""
    You are an expert editor focued om clarity and simplicity.
    Your job is to elimate ambiguty, redundancy, and make every sentence crisp and clear.
    Don't worry about persuasion or tone - just maek the message easy to read and understand.
    """
)

tone_agent = AssistantAgent(
    "ToneAgent",
    model_client=model,
    system_message="""
    You are a communication coach focued on emotional tone and professionalism.
    Your job is to make email sound warm, confident, and human - while staying professional.
    and appropriate for the audience. Improve the emotional reasonance, polish the phrasing,
    and adjust any words that may come off ass stiff, cold, or overly casual.
    """
)

persuasion_agent = AssistantAgent(
    "PersuasionAgent",
    model_client=model,
    system_message="""
    You are a persuasion expert trained in marketing, behavior psychology, and copywriting.
    Your job is to enhance the email's persuasive power: improve call to action,
    structure arguuemnts, and emphasize benefits. Remove weak or passive language.
    """
)

synthesizer_agent = AssistantAgent(
    "SynthesizerAgent",
    model_client=model,
    system_message="""
    You are an advanced email-writing speciallist. Your role is to read all prior agent responses and revisions, ad then
    **synthesize the best ideas** into a unfied,
    polished draft of the email. Focus on : Integrating clarity, tone, and persuasion improvements;
    Ensuring coherence, fluency, and natural voice; Creating a version that feels professional, effective, and readable.
    """
)

critic_agent = AssistantAgent(
    "CriticAgent",
    model_client=model,
    system_message="""
    You are an email quaility evaluator. Your job is perform a final review
    of the synthesized email and determine if it meets professional standards.
    Review the email for:

    Clarity and flow, appropriate professional tone, effective call-to-action, and overall
    coherence.
    Be constructive but decisive. If the email has major flows(unclear message, unprofessional tone, or missing key elements),
    provide ONE specific improvement suggestion, if the email meets professional standards
    and communicates effectively, respond with 'The email meets professional standards' followed by `TERMINATE` on a new line.
    You should approve emails that are perfect enough for professional use. don't settle.
    """
)

text_termination = TextMentionTermination("TERMINATE")
max_message_termination = MaxMessageTermination(max_messages=30)

termination_conditions = text_termination | max_message_termination

team = RoundRobinGroupChat(
    participants=[
        clarity_agent,
        tone_agent,
        persuasion_agent,
        synthesizer_agent,
        critic_agent,
    ],
    termination_condition=termination_conditions,
)

async def main():
    await Console(
        team.run_stream(task="안녕 나는 배고파, 점심을 사줘 그리고 내 사업에 투자해줘, ㄱㅅ")
    )

if __name__ == "__main__":
    asyncio.run(main())