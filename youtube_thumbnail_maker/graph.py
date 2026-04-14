from langgraph.graph import END, START, StateGraph
from typing import TypedDict
from langgraph.types import Send, interrupt, Command
import subprocess
from openai import OpenAI
import textwrap
from langchain.chat_models import init_chat_model
import operator
from typing_extensions import Annotated
import base64
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model("openai:gpt-4o-mini",)

class State(TypedDict):
    video_file : str
    audio_file : str
    transcription : str
    summaries : Annotated[list[str], operator.add]
    thumbnail_prompts : Annotated[list[str], operator.add]
    thumbnail_sketches : Annotated[list[bytes], operator.add]
    final_summary : str
    user_feedback : str
    chosen_prompt : str

def extract_audio(state: State):
    output_file = state["video_file"].replace("mp4", "mp3")
    command = [
        "ffmpeg",
        "-i",
        state["video_file"],
        "-filter:a",
        "atempo=2.0",
        "-y",
        output_file

    ]

    subprocess.run(command)

    return {"audio_file": output_file}

def transcribe_audio(state: State):
    client = OpenAI()
    with open(state["audio_file"], "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file,
        )

        return {
            "transcription": transcription
        }
    

def dispatch_summarizers(state: State):
    transcription = state["transcription"]
    chunks = []

    for i, chunk in enumerate(textwrap.wrap(transcription, 500)):
        chunks.append(
            {
                "id": i + 1,
                "chunk": chunk
            }
        )
    return [
        Send(
            "summarize_chunk",
            chunk
        ) for chunk in chunks
    ]

def summarize_chunk(chunk):
    chunk_id = chunk["id"]
    chunk_content = chunk["chunk"]

    print(f"Summarizing chunk {chunk_id}...")

    response = llm.invoke(
        f"""
        Summarize following content in Korean.
        자연스럽고 이해하기 쉬운 한글 요약본으로 작성해줘.

        Text: {chunk_content}
        """
    )

    summary = f"[Chunk {chunk_id}]: {response.content}"

    return {
        "summaries" : [summary]
    }

def mega_summary(state : State):
    all_summaries = "\n".join(state["summaries"])

    prompt = f"""

    Summarize the following summaries into one summary in Korean.
    자연스럽고 이해하기 쉬운 한글 요약본으로 작성해줘.

    Invidiual summaries:

    {all_summaries}
    """
    response = llm.invoke(prompt)

    return {
        "final_summary": response.content
    }

def dispatch_artists(state: State):
    return[
        Send(
            "generate_thumbnails",{
                "id": i,
                "summary" : state["final_summary"]
            }
        ) for i in range(5)
    ]


def generate_thumbnails(args):
    id = args["id"]
    summary = args["summary"]

    prompt = f"""
    Bseed on this video summary, create a detialed visual prompt for a youtube thumbnail. 

    Create a detailed prompt for generating a thumbnail image that would attract viewers. Include

       - Main visual elements
       - Color scheme
       - Text overlay suggestions( Korean )
       - Overall composition

    Summary: {summary}

    """

    response = llm.invoke(prompt)

    thumbnail_prompt = response.content

    client = OpenAI()

    result = client.images.generate(
        model="gpt-image-1.5",
        prompt=thumbnail_prompt,
        quality="low",
        moderation="low",
        size="auto",
    )

    image_bytes = base64.b64decode(result.data[0].b64_json)

    file_name = f"thumbnail_{id}.png"

    with open(file_name, "wb") as image_file:
        image_file.write(image_bytes)

        return {
            "thumbnail_prompts": [thumbnail_prompt],
            "thumbnail_sketches": [file_name]
        }
    
def human_feedback(state: State):
    answer = interrupt({
        "chosen_thumbnail" : "가장 마음에 드는 썸네일을 선택해주세요.",
        "feedback" : "선택한 썸네일에 대한 피드백을 남겨주세요."
    })
    user_feedback = answer["user_feedback"]
    chosen_prompt = answer["chosen_prompt"]

    return {
        "user_feedback": user_feedback,
        "chosen_prompt": state["thumbnail_prompts"][chosen_prompt]
    }

def generate_hd_thumbnail(state: State):
    chosen_prompt = state["chosen_prompt"]
    user_feedback = state["user_feedback"]

    prompt = f"""
    You are a professional Youtube thumbnail designer.
    Take this orignal thumbnail prompt and user feedback to create an improved thumbnail prompt that would attract more viewers.

    Original thumbnail prompt: {chosen_prompt}
    User feedback: {user_feedback}
    

    Create an enhanced prompt that:

        1. Maintains the core concept from the otiginal prompt.
        2. Specifically addresses the user feedback to improve the thumbnail's appeal.
        3. Adds professional Youtube thumbnail specifications

            - High contrast and bold visual elements
            - Clear focal points that draw eye
            - Optimal text placement and readability with generous padding from edges

            _ IMPORTANT : Always ensure adequate white space/padding between any text and the image borders

    """

    response = llm.invoke(prompt)

    final_thumbnail_prompt = response.content

    client = OpenAI()

    result = client.images.generate(
        model="gpt-image-1.5",
        prompt=final_thumbnail_prompt,
        quality="high",
        moderation="low",
        size="auto",
    )


    image_bytes = base64.b64decode(result.data[0].b64_json)

    with open("final_thumbnail.png", "wb") as image_file:
        image_file.write(image_bytes)

graph_builder = StateGraph(State)

graph_builder.add_node("extract_audio", extract_audio)
graph_builder.add_node("transcribe_audio", transcribe_audio)
graph_builder.add_node("summarize_chunk", summarize_chunk)
graph_builder.add_node("mega_summary", mega_summary)
graph_builder.add_node("generate_thumbnails", generate_thumbnails)
graph_builder.add_node("human_feedback", human_feedback)
graph_builder.add_node("generate_hd_thumbnail", generate_hd_thumbnail)

graph_builder.add_edge(START, "extract_audio")
graph_builder.add_edge("extract_audio", "transcribe_audio")
graph_builder.add_conditional_edges("transcribe_audio", dispatch_summarizers, ["summarize_chunk"])
graph_builder.add_edge("summarize_chunk", "mega_summary")
graph_builder.add_conditional_edges("mega_summary", dispatch_artists, ["generate_thumbnails"])
graph_builder.add_edge("generate_thumbnails", "human_feedback")
graph_builder.add_edge("human_feedback", "generate_hd_thumbnail")
graph_builder.add_edge("generate_hd_thumbnail", END)

graph = graph_builder.compile(name="youtube_thumbnail_maker")




