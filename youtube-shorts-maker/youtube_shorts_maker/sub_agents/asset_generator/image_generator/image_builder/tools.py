from google.adk.tools.tool_context import ToolContext
from google import genai
from google.genai import types
import asyncio

client = genai.Client()


async def generate_images(tool_context: ToolContext):
    print("DEBUG: generate_images tool called")
    prompt_builder_output = tool_context.state.get("prompt_builder_output")

    optimized_prompts = prompt_builder_output.get("optimized_prompts")

    existing_artifacts = await tool_context.list_artifacts()

    generated_images_list = []
    

    for prompt in optimized_prompts:
        scene_id = prompt.get("scene_id")
        enhanced_prompt = prompt.get("enhanced_prompt")
        file_name = f"scene_{scene_id}_image.jpeg"

        if file_name in existing_artifacts:
            generated_images_list.append(
                {"scene_id": scene_id, "prompt": enhanced_prompt[:100]}
            )
            # Optional: Check if file exists in output dir and copy if missing, but let's stick to generation flow for now.
            continue

        # Retry logic for 503 errors
        max_retries = 3
        retry_delay = 5  # seconds
        success = False
        
        for attempt in range(max_retries):
            try:
                result = client.models.generate_images(
                    model="imagen-4.0-generate-001",
                    prompt=enhanced_prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        output_mime_type="image/jpeg",
                        aspect_ratio="9:16",
                    ),
                )
                
                if not result.generated_images or not result.generated_images[0].image:
                    print(f"Error: 이미지가 생성되지 않았습니다 (Attempt {attempt+1}) - {file_name}")
                    continue # Try next attempt or fail if logic allows, but here it's API success with empty data
                
                # Success
                image_bytes = result.generated_images[0].image.image_bytes

                artifact = types.Part(
                    inline_data=types.Blob(
                        mime_type="image/jpeg",
                        data=image_bytes,
                    )
                )

                await tool_context.save_artifact(
                    filename=file_name,
                    artifact=artifact,
                )
                
                generated_images_list.append({"scene_id": scene_id, "prompt": enhanced_prompt[:100]})
                success = True
                break # Exit retry loop
                
            except Exception as e:
                print(f"Warning: API call failed for {file_name} (Attempt {attempt+1}/{max_retries}). Error: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2 # Exponential backoff
                else:
                    print(f"Error: Failed to generate image for {file_name} after {max_retries} attempts.")

    return {
        "total_images": generated_images_list,
        "status": "complete",
    }