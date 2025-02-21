import os
import json
import logging
from openai import OpenAI
import re
import base64
from feature_detection import extract_features

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI client initialization
client = OpenAI()

# Ensure the OpenAI API key is set
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set in environment variables.")
    raise EnvironmentError("Missing OPENAI_API_KEY.")

client.api_key = OPENAI_API_KEY

# Default images for fallback
DEFAULT_CARD_IMAGE = "https://example.com/default_card.png"
DEFAULT_MEME_IMAGE = "https://media1.giphy.com/media/hECJDGJs4hQjjWLqRV/giphy.gif?cid=6c09b952gwxhe22lcif92104ht5gph5qu62jbs7acqq8o4p9&ep=v1_gifs_search&rid=giphy.gif&ct=g"


async def analyze_user_input(user_input: str) -> dict:
    print("=========user_input=========", user_input)
    """
    Analyzes user input and generates a response using the OpenAI API.

    Args:
        user_input (str): The user's input message.

    Returns:
        dict: A dictionary containing the response type and content, or an error message.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": """
                            {
                                "name": "Predict Tarot Card from Text Sentiment",
                                "description": "This system analyzes the sentiment of the input text and predicts a tarot card, initiates a conversation, or generates a meme based on the sentiment and context. The input might mostly be in Thai, so responses should match the input language.",
                                "steps": [
                                    {
                                    "step": "Sentiment Analysis",
                                    "action": "Analyze the sentiment of the given text (positive, negative, neutral) using text analysis techniques. The input might mostly be in Thai."
                                    },
                                    {
                                    "step": "Determine Response Type",
                                    "action": "Based on the sentiment and context, decide the response type: tarot card prediction, conversational response, or meme suggestion. Need to select only one answer type; do not return an array."
                                    },
                                    {
                                    "step": "Tarot Card Selection",
                                    "action": "If the answer type is 'card', select a random tarot card from the Major Arcana (0-XXI) and return an image from the provided list.",
                                    "images": [
                                        {
                                            "name": "XIV.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619434/vahjqteh7yv41kgo58bq.jpg"
                                        },
                                        {
                                            "name": "III.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619436/cx1rxypkzo8r9obzgcu2.jpg"
                                        },
                                        {
                                            "name": "I.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619436/ylvr8vjpl09grcpjufob.jpg"
                                        },
                                        {
                                            "name": "VI.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619437/o4rzusteygd4twzygcal.jpg"
                                        },
                                        {
                                            "name": "VII.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619439/tlfum4e37hcozutsxvxl.jpg"
                                        },
                                        {
                                            "name": "XV.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619439/dtdi8rcywfgzdsukz4jk.jpg"
                                        },
                                        {
                                            "name": "X.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619440/k5cafz3xi9z7wfywpqba.jpg"
                                        },
                                        {
                                            "name": "XIII.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619442/rmzqttnjtyezvpdwtze1.jpg"
                                        },
                                        {
                                            "name": "IX.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619443/vb90e7jbmljqawr0qsdz.jpg"
                                        },
                                        {
                                            "name": "XXI.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619443/xsxjtvymqnlid7mfqvgq.jpg"
                                        },
                                        {
                                            "name": "II.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619445/xcxbhpptmfeool6xubpn.jpg"
                                        },
                                        {
                                            "name": "XVIII.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619446/gapo7gqqpmppppfm39wp.jpg"
                                        },
                                        {
                                            "name": "XVII.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619447/sm8oeyjm58w283uyxkju.jpg"
                                        },
                                        {
                                            "name": "VIII.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619448/ybutnri9i1x8sgopor7b.jpg"
                                        },
                                        {
                                            "name": "XVI.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619449/onifs9cuzhfalmxya3qw.jpg"
                                        },
                                        {
                                            "name": "IV.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619450/vpw9dkvtf6iupjimfx5m.jpg"
                                        },
                                        {
                                            "name": "XII.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619451/okjurztgfssnrqaxniyi.jpg"
                                        },
                                        {
                                            "name": "V.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619453/fx66qkbq5xplbxopthyd.jpg"
                                        },
                                        {
                                            "name": "XX.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619454/jx8age5z8ag80g5l78mp.jpg"
                                        },
                                        {
                                            "name": "XIX.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619455/k5qcy8vfjkddory2ze5i.jpg"
                                        },
                                        {
                                            "name": "XI.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619456/w6kivdlgq5frgmwxnjta.jpg"
                                        },
                                        {
                                            "name": "0.jpg",
                                            "url": "https://res.cloudinary.com/dy0x2zlmm/image/upload/v1734619457/q0ijgklymbjpp3efplna.jpg"
                                        }
                                    ]
                                    },
                                    ",
                                        "conditions": [
                                            {
                                            "condition": "If sentiment is neutral or negative and context suggests conversation",
                                            "response": {
                                                "answer_type": "chit-chat",
                                                "response": {
                                                "text": "Provide a conversational response to engage the user."
                                                }
                                            }
                                            },
                                            {
                                            "condition": "If sentiment analysis indicates a clear emotional direction positive ",
                                            "response": {
                                                "answer_type": "card",
                                                "response": {
                                                "image_link": "<appropriate_tarot_card_image>.png",
                                                "text": "Provide provide a brief description of the card based on sentiment and then engage the user in a conversation."
                                                }
                                            }
                                            },
                                            {
                                            "condition": "If sentiment suggests humor or light-heartedness",
                                            "response": {
                                                "answer_type": "meme",
                                                "response": {
                                                "image_link": "Provide gif meme link that existing in internext base on user sentimental make sure it can open in telegram."
                                                }
                                            }
                                            }
                                        ]
                                        },
                                        {
                                        "step": "Generate Response",
                                        "action": "Return the generated response based on the determined response type."
                                        }
                                    ]
                                    }

                                    """
                                    
                        }
                    ],
                },
                {"role": "user", "content": [{"type": "text", "text": user_input}]},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "sentiment",
                    "strict": False,
                    "schema": {
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "properties": {
                            "answer_type": {
                                "type": "string",
                                "enum": ["card", "chit-chat", "meme"],
                                "description": "The type of response based on sentiment and context analysis."
                            },
                            "response": {
                                "type": "object",
                                "properties": {
                                    "text": {
                                        "type": "string",
                                        "description": "The conversational response text, required if 'answer_type' is 'chit-chat' or 'card'."
                                    },
                                    "image_link": {
                                        "type": "string",
                                        "format": "uri",
                                        "description": "The link to an image, required if 'answer_type' is 'card' or 'meme'."
                                    }
                                },
                                "required": ["text"],
                                "anyOf": [
                                    {"required": ["text"]},
                                    {"required": ["image_link"]}
                                ]
                            }
                        },
                        "required": ["answer_type", "response"]
                    }
                }
            },
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        print("=========response=========", response)

        # Parse the assistant's response
        assistant_reply = response.choices[0].message.content
        print("=========assistant_reply=========", assistant_reply)
        return json.loads(assistant_reply)

    except Exception as e:
        logger.error(f"Error processing OpenAI response: {e}")
        return {
            "error": "An error occurred while processing your input. Please try again."
        }


async def analyze_user_audio_input(audio_file_path: str) -> dict:
    """Processes a single audio file asynchronously by transcribing and detecting emotions."""
    try:
        # ✅ Extract features
        features = extract_features(audio_file_path)
        if not features:
            logger.error(f"Feature extraction failed for {audio_file_path}")
            return {"error": "Feature extraction failed."}
        print(f"✅ Features extracted is {features}")

        # ✅ Read and encode audio file in base64
        with open(audio_file_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode("utf-8")

        # ✅ Prepare feature data as a string
        feature_text = json.dumps(features, indent=2)

        response = client.chat.completions.create(
            model="gpt-4o-audio-preview",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI designed for emotional support. Always remember the user's previous responses within the session to maintain conversation continuity. Use the last transcript to provide contextually relevant responses."
                        "to extract emotions based on Ekman's theory (anger, disgust, fear, happiness, sadness, surprise, and neutral). "
                        "Additionally, you detect early signs of depression based on linguistic patterns and acoustic features.\n\n"
                        "The input might mostly be in Thai. You should be able to understand and respond in Thai as well."

                        "**Instructions:**\n"
                        "- Always return a valid JSON object **without** any formatting or extra text.\n"
                        "- The JSON object **must include**: `transcription`, `emotion`, `depression_score`, and `ai_response`.\n"
                        "- The analysis is performed using both:\n"
                        "  - **Text-based features**: Sentiment, pronoun usage, negative word frequency, linguistic markers.\n"
                        "  - **Acoustic features**: Speech rate, pitch, intonation, and pauses.\n"

                        "**Response Style: Empathetic & Supportive**\n"
                        "- Your responses should be warm, understanding, and emotionally validating.\n"
                        "- Acknowledge the user's feelings before offering any help.\n"
                        "- Ask open-ended questions to encourage deeper engagement.\n"

                        "**Example Output:**\n"
                        "{\n"
                        '  "transcription": "ฉันรู้สึกเหนื่อยและไม่มีความหวังเลย",\n'
                        '  "emotion": {"sadness": 0.75, "neutral": 0.15, "anger": 0.10},\n'
                        '  "depression_score": 0.85,\n'
                        '  "ai_response": "ฉันเข้าใจนะว่าคุณกำลังรู้สึกหนักใจ มันไม่ผิดที่จะรู้สึกแบบนี้นะ ลองหายใจลึก ๆ แล้วเล่าให้ฉันฟังเพิ่มเติมได้ไหม?"\n'
                        "}\n"

                        "- **Do not include backticks (`) or Markdown formatting in the response.**"
                    )
                    }
                    ,
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

        # ✅ Log raw response for debugging
        logger.info(f"Raw API Response: {response}")

        # ✅ Check if response contains expected data
        if not response.choices or not response.choices[0].message:
            logger.error("OpenAI API returned an empty response or missing choices.")
            return {"error": "OpenAI API returned an unexpected response."}

        # ✅ Extract response content
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
