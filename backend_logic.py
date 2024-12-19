import os
import random
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Tarot card data
tarot_cards = {
    "The Fool": "New beginnings, optimism, trust in life",
    "The Magician": "Power, potential, and the unification of the physical and spiritual worlds",
    "The High Priestess": "Intuition, mystery, and understanding",
    "The Empress": "Fertility, femininity, beauty, nature",
    "The Emperor": "Authority, structure, control",
    "The Hierophant": "Tradition, conformity, and spiritual guidance",
    "The Lovers": "Love, relationships, and harmony",
    "The Chariot": "Control, willpower, and success",
    "Strength": "Courage, patience, and inner strength",
    "The Hermit": "Introspection, contemplation, and seeking guidance",
    "Wheel of Fortune": "Change, cycles, and destiny",
    "Justice": "Justice, fairness, and truth",
}

def determine_tarot_card():
    """Randomly select a tarot card and its meaning."""
    card, meaning = random.choice(list(tarot_cards.items()))
    return card, meaning

def get_user_emotion(user_input):
    """Analyze the sentiment of the user's input."""
    try:
        emotion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with a user context, and your task is to classify its sentiment as positive, neutral, or negative."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1
        )
        return emotion.choices[0].message.content
    except Exception as e:
        return f"Error in sentiment analysis: {str(e)}"

def get_tarot_reading(question, card, meaning):
    """Generate a tarot reading response based on the question and card."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with a tarot card and its meaning. Your task is to respond like a tarot reader while subtly assessing if the individual requires mental health support in the background. If an individual needs support, you keep asking questions; otherwise, say thank you and bless them to have a good day."
                },
                {
                    "role": "user",
                    "content": f"{question} {card} {meaning}"
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in tarot reading generation: {str(e)}"
