import os
import json
import logging
from openai import OpenAI

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
                                "description": "This system analyzes the sentiment of the input text and predicts a tarot card, initiates a conversation, or generates a meme based on the sentiment and context. I welcome you to interact with me! and i very kind and responsive",
                                "steps": [
                                    {
                                    "step": "Sentiment Analysis",
                                    "action": "Analyze the sentiment of the given text (positive, negative, neutral) using text analysis techniques.",
                                    "output": "sentiment_type (positive, negative, neutral)"
                                    },
                                    {
                                    "step": "Determine Response Type",
                                    "action": "Based on the sentiment and context, decide the response type: tarot card prediction, conversational response, or meme suggestion. Need to select only one answer type; do not give an array. if type is tarot card prediction then provide random tarot card number from Major Arcana(0-XXI). select image from this [
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

                                """,
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
                                "description": "The type of response based on sentiment and context analysis.",
                            },
                            "response": {
                                "type": "object",
                                "properties": {
                                    "text": {
                                        "type": "string",
                                        "description": "The conversational response text, required if 'answer_type' is 'ชวนคุย' or 'card' ",
                                    },
                                    "image_link": {
                                        "type": "string",
                                        "format": "uri",
                                        "description": "The link to an image, required if 'answer_type' is 'card' or 'meme'.",
                                    },
                                },
                                "required": ["text"],
                                "anyOf": [
                                    {"required": ["text"]},
                                    {"required": ["image_link"]},
                                ],
                            },
                        },
                        "required": ["answer_type", "response"],
                    },
                },
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
