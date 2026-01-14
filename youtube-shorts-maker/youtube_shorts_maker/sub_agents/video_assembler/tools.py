import os
import subprocess
import tempfile
from google.adk.tools.tool_context import ToolContext
from google.genai import types

async def assemble_video(tool_context: ToolContext):
    """
    Assembles a high-quality YouTube Shorts video (1080x1920, 30fps) from generated assets.

    This tool automatically retrieves the scene information from the shared state 
    ('content_planner_output') and the corresponding image/audio artifacts.

    Process:
    1. **Clip Generation**: For each scene, creates a temporary .mp4 clip.
       - The image is looped to match the exact duration of the audio (narration).
       - The image is scaled to 1080x1920 (9:16 aspect ratio).
       - Frame rate is forced to 30fps.
    2. **Concatenation**: Merges all individual clips into a final seamless video file.

    Args:
        tool_context (ToolContext): The ADK tool context.

    Returns:
        Dict[str, Any]: Result of the operation including the path to the final video.
    """
    
    # Retrieve scenes from shared state
    content_plan = tool_context.state.get("content_planner_output", {})
    scenes = content_plan.get("scenes", [])
    
    if not scenes:
        print("Error: No scenes found in 'content_planner_output'.")
        return {"success": False, "error": "No scenes found in state."}

    print(f"Starting video assembly for {len(scenes)} scenes...")
    
    # Create a temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        input_clips = []
        
        # 1. Process each scene to create individual clips
        for i, scene in enumerate(scenes):
            scene_id = i + 1 # Assume 1-based indexing for files
            
            # FORCE correct filenames based on established convention
            image_file = f"scene_{scene_id}_image.jpeg"
            audio_file = f"scene_{scene_id}_narration.wav"

            print(f"Processing Scene {scene_id}: {image_file} + {audio_file}")

            try:
                # Retrieve assets strictly from ToolContext
                image_path = await _get_artifact_path(tool_context, image_file, temp_dir)
                audio_path = await _get_artifact_path(tool_context, audio_file, temp_dir)
            except Exception as e:
                print(f"Error preparing assets for scene {scene_id}: {e}")
                continue

            output_clip = os.path.join(temp_dir, f"clip_{i}.mp4")
            
            # FFmpeg command to create a clip from image and audio
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", image_path,
                "-i", audio_path,
                "-c:v", "libx264", "-tune", "stillimage",
                "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
                "-r", "30",
                "-shortest",
                output_clip
            ]
            
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                input_clips.append(output_clip)
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg error for scene {i+1}: {e.stderr.decode()}")
                continue

        if not input_clips:
            return {"success": False, "error": "No clips were generated. Please check if image and audio assets exist."}

        # 2. Concatenate clips
        list_file_path = os.path.join(temp_dir, "list.txt")
        with open(list_file_path, "w") as f:
            for clip in input_clips:
                f.write(f"file '{clip}'\n")

        final_output_filename = "final_video.mp4"
        final_output_path = os.path.join(temp_dir, final_output_filename)

        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file_path,
            "-c", "copy",
            final_output_path
        ]

        try:
            print("Concatenating clips...")
            subprocess.run(concat_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 3. Save final artifact
            with open(final_output_path, "rb") as video_file:
                video_data = video_file.read()
            
            artifact = types.Part(
                inline_data=types.Blob(
                    mime_type="video/mp4",
                    data=video_data
                )
            )
            
            await tool_context.save_artifact(
                filename=final_output_filename,
                artifact=artifact
            )
            
            # Also save to local output directory for visibility
            local_output_dir = "output/videos"
            os.makedirs(local_output_dir, exist_ok=True)
            local_path = os.path.join(local_output_dir, final_output_filename)
            with open(local_path, "wb") as f:
                f.write(video_data)
                
            print(f"Video assembly complete. Saved to {local_path} and artifacts.")
            
            return {
                "success": True,
                "filename": final_output_filename,
                "local_path": local_path
            }

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg concat error: {e.stderr.decode()}")
            return {"success": False, "error": f"Concat failed: {e.stderr.decode()}"}


async def _get_artifact_path(tool_context: ToolContext, filename: str, temp_dir: str) -> str:
    """
    Retrieves an artifact strictly from ToolContext and saves it to a temporary directory.
    
    Args:
        tool_context (ToolContext): The ADK tool context.
        filename (str): The name of the artifact file.
        temp_dir (str): The temporary directory to save the file in.

    Returns:
        str: The full path to the saved file in the temporary directory.

    Raises:
        RuntimeError: If the artifact cannot be retrieved or contains no data.
    """
    try:
        # Retrieve the artifact from the context
        # Assumes load_artifact returns a Google GenAI Part object or similar structure
        artifact = await tool_context.load_artifact(filename)
        
        if artifact is None:
            raise ValueError(f"Artifact '{filename}' not found in ToolContext.")

        data = None
        
        # Extract binary data based on the artifact structure
        if hasattr(artifact, 'inline_data') and artifact.inline_data:
             data = artifact.inline_data.data
        
        if data is None:
            raise ValueError(f"Artifact '{filename}' has no data content.")

        temp_path = os.path.join(temp_dir, filename)
        with open(temp_path, "wb") as f:
            f.write(data)
            
        return temp_path

    except Exception as e:
        error_msg = f"Failed to retrieve artifact '{filename}' from ToolContext: {str(e)}"
        # Re-raise as RuntimeError to signal failure to the caller
        raise RuntimeError(error_msg) from e