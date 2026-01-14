from google.adk.tools.tool_context import ToolContext
from google import genai
from google.genai import types
import os
import io
import wave
import asyncio
from typing import List, Dict, Any

client = genai.Client()

async def generate_narrations(tool_context: ToolContext, voice: str, voice_instructions: List[Dict[str, Any]]):
    """
    Generates high-quality narration audio files for each scene using Google GenAI's Native TTS.

    Args:
        tool_context (ToolContext): The ADK tool context providing access to shared state and artifacts.
        voice (str): The name of the Gemini prebuilt voice to use. 
            Options: 'Puck' (Energetic), 'Charon' (Deep), 'Kore' (Friendly), 'Fenrir' (Storytelling), 'Aoede' (Artistic).
        voice_instructions (List[Dict[str, Any]]): A list of dictionaries containing narration details for each scene.
            Each dictionary should include:
            - 'scene_id' (int): The unique identifier for the scene.
            - 'input' (str): The exact text script to be converted to speech.
            - 'instructions' (str): Guidance on the tone, speed, or mood for the narration.

    Returns:
        Dict[str, Any]: A status report containing:
            - 'status': 'complete' if successful.
            - 'generated_audio_files': List of dicts with 'scene_id' and 'file_path'.
            - 'total_files': Total number of audio files successfully generated.
    """
    existing_artifacts = await tool_context.list_artifacts()

    generated_narrations = []

    for instruction in voice_instructions:
        text_input = instruction.get("input")
        instructions = instruction.get("instructions", "")
        scene_id = instruction.get("scene_id")
        
        if scene_id is None or text_input is None:
            continue
            
        # Back to .wav for quality and simplicity
        filename = f"scene_{scene_id}_narration.wav"

        if filename in existing_artifacts:
            generated_narrations.append({
                'scene_id' : scene_id,
                'filename' : filename,
                'input' : text_input,
                'instructions' : (instructions or "")[:50]
            })
            continue

        # Retry logic
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash-preview-tts",
                    contents=text_input,
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=voice
                                )
                            )
                        )
                    )
                )

                if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                    part = response.candidates[0].content.parts[0]
                    if part.inline_data:
                        pcm_data = part.inline_data.data
                        
                        if pcm_data is None:
                            print(f"Warning: pcm_data is None for scene {scene_id}")
                            continue

                        # Convert raw PCM (24kHz, 16-bit mono) to WAV
                        wav_buffer = io.BytesIO()
                        with wave.open(wav_buffer, 'wb') as wav_file:
                            wav_file.setnchannels(1) # Mono
                            wav_file.setsampwidth(2) # 16-bit
                            wav_file.setframerate(24000)
                            wav_file.writeframes(pcm_data)
                        
                        wav_bytes = wav_buffer.getvalue()

                        artifact = types.Part(
                            inline_data=types.Blob(
                                mime_type="audio/wav",
                                data=wav_bytes
                            )
                        )

                        await tool_context.save_artifact(
                            filename=filename,
                            artifact=artifact,
                        )
                        
                        generated_narrations.append({
                            'scene_id' : scene_id,
                            'filename' : filename,
                            'input' : text_input,
                            'instructions' : (instructions or "")[:50]
                        })
                        break # Success, exit retry loop
                    else:
                        print(f"Warning: No inline audio data for scene {scene_id}")
                else:
                    print(f"Warning: Empty response for scene {scene_id}")

            except Exception as e:
                print(f"Error generating audio for scene {scene_id} (Attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"Failed to generate audio for scene {scene_id} after all attempts.")

    return {
        "sucess" : True,
        "narrations" : generated_narrations
    }
