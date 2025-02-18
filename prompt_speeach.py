import os
import json
import logging
import base64
import asyncio
from openai import OpenAI
from sklearn.metrics import classification_report

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prompt_speech")

# Load dataset labels (ground truth)
label_file_path = "emotion_label.json"  # Ensure this file is in the working directory
with open(label_file_path, "r") as f:
    emotion_labels = json.load(f)

# Extract and normalize ground truth labels
ground_truth = {file: annotations[0]["majority_emo"].lower() for file, annotations in emotion_labels.items()}

# OpenAI client initialization
client = OpenAI()

# Ensure API key is available
if not os.getenv("OPENAI_API_KEY"):
    logger.error("OPENAI_API_KEY is not set in environment variables.")
    raise EnvironmentError("Missing OPENAI_API_KEY.")

import re
import json
import logging

logger = logging.getLogger("prompt_speech")

async def analyze_user_audio_input(audio_file_path: str) -> dict:
    """Processes a single audio file asynchronously by transcribing and detecting emotions."""
    try:
        # Read audio file and encode it in base64
        with open(audio_file_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4o-audio-preview",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant that processes audio input by first transcribing it into text and then analyzing the text "
                        "to extract emotions based on Ekman's theory (anger, disgust, fear, happiness, sadness, surprise, and neutral). "
                        "It also detects early signs of depression based on linguistic patterns.\n\n"
                        "**Instructions:**\n"
                        "- Always return a valid JSON object **without** any formatting or extra text.\n"
                        "- The JSON object **must include**: `transcription`, `emotion`, and `depression_indicator`.\n"
                        "- Example response:\n"
                        "{\n"
                        '  "transcription": "The transcribed speech here.",\n'
                        '  "emotion": "neutral",\n'
                        '  "depression_indicator": false\n'
                        "}\n"
                        "- **Do not include backticks (`) or Markdown formatting in the response.**"
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": audio_data,
                                "format": "wav"
                            }
                        }
                    ]
                }
            ],
            modalities=["text"],
            temperature=1,
            max_completion_tokens=2048
        )

        # Log raw response for debugging
        logger.info(f"Raw API Response: {response}")

        # Check if response contains expected data
        if not response.choices or not response.choices[0].message:
            logger.error("OpenAI API returned an empty response or missing choices.")
            return {"error": "OpenAI API returned an unexpected response."}

        # Extract response content
        assistant_reply = response.choices[0].message.content.strip()
        if not assistant_reply:
            logger.error("Assistant Reply is empty. OpenAI may not have processed the request correctly.")
            return {"error": "Assistant Reply is empty."}

        logger.info(f"Assistant Reply: {assistant_reply}")

        # ✅ Remove triple backticks if they exist
        assistant_reply = re.sub(r"```json\n(.*?)\n```", r"\1", assistant_reply, flags=re.DOTALL)

        # ✅ Attempt to parse JSON
        return json.loads(assistant_reply)

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error. Response was: {assistant_reply}")
        return {"error": "Failed to parse API response.", "response_text": assistant_reply}
    except Exception as e:
        logger.error(f"Error processing OpenAI response for {audio_file_path}: {e}")
        return {"error": "An unexpected error occurred."}  

async def batch_process_audio(audio_files):
    """Processes multiple audio files asynchronously using OpenAI API."""
    tasks = [analyze_user_audio_input(file) for file in audio_files]
    return await asyncio.gather(*tasks)

async def evaluate_accuracy(audio_files):
    """Evaluates accuracy by directly matching OpenAI's predictions with dataset labels using index."""
    y_true = []
    y_pred = {}
    predictions = {}

    # Normalize filenames (convert .wav to .flac for matching with ground truth)
    filenames = [os.path.basename(file).replace(".wav", ".flac").strip() for file in audio_files][:5]  # ✅ Limit to 5

    # Convert ground truth to a list of labels (ignoring filenames)
    ground_truth_labels = [annotations[0]["majority_emo"].lower() for _, annotations in emotion_labels.items()][:5]  # ✅ Limit to 5

    # Get OpenAI responses (only 5)
    openai_responses = (await batch_process_audio(audio_files))[:5]  # ✅ Limit to 5

    # Ensure the length matches
    if len(openai_responses) != len(ground_truth_labels):
        print(f"⚠️ Mismatch: Expected {len(ground_truth_labels)} responses, but got {len(openai_responses)}", flush=True)
        return {"error": "Mismatch in OpenAI responses and ground truth labels."}, {}

    # Assign responses using index matching
    for idx in range(5):
        response = openai_responses[idx]
        ground_truth_emotion = ground_truth_labels[idx]  # Get ground truth emotion at the same index

        if "emotion" in response:
            predicted_emotion = response["emotion"].lower()
            y_true.append(ground_truth_emotion)
            y_pred[idx] = predicted_emotion
            predictions[idx] = response

            print(f"✅ Matched: {ground_truth_emotion} == {predicted_emotion}", flush=True)
        else:
            predictions[idx] = {"error": "Invalid response", "details": response}
            print(f"❌ Error processing index {idx} → {response.get('error', 'Unknown error')}", flush=True)

    print("\n===== OpenAI Predictions (First 5) =====", flush=True)
    print(list(predictions.items()), flush=True)


    if not y_pred:
        print("⚠️ No predictions were made. Please check API responses and dataset alignment.", flush=True)
        return {"error": "No valid predictions available."}, predictions 
    report = classification_report(y_true, list(y_pred.values()), output_dict=True)

    with open("openai_predictions.json", "w") as f:
        json.dump(predictions, f, indent=4)

    return report, predictions 
