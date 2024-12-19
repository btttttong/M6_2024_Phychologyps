from openai import OpenAI
import json
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Initialize OpenAI client

def mood_to_tarot_mapping(mood):
    # Predefined mood-to-tarot mapping
    tarot_map = {
    "Optimistic": {
        "name": "The Sun",
        "description": "The Sun card represents optimism, success, and positivity.",
        "advice": "Embrace the light and let your positivity guide you through challenges."
    },
    "Reflective": {
        "name": "The Moon",
        "description": "The Moon represents intuition, mystery, and the subconscious mind.",
        "advice": "Trust your intuition and explore hidden aspects of your situation."
    },
    "Confident": {
        "name": "The Emperor",
        "description": "The Emperor symbolizes authority, structure, and stability.",
        "advice": "Take control of your situation and act with confidence and discipline."
    },
    "Anxious": {
        "name": "The Tower",
        "description": "The Tower represents sudden change, upheaval, and revelations.",
        "advice": "Embrace the changes ahead and find strength in the chaos."
    },
    "Hopeful": {
        "name": "The Star",
        "description": "The Star card represents hope, inspiration, and renewal.",
        "advice": "Stay true to your dreams and believe in the possibilities ahead."
    },
    "Determined": {
        "name": "The Chariot",
        "description": "The Chariot symbolizes determination, willpower, and triumph over obstacles.",
        "advice": "Stay focused on your goals and let your determination guide you."
    },
    "Calm": {
        "name": "The High Priestess",
        "description": "The High Priestess represents intuition, wisdom, and serenity.",
        "advice": "Trust your inner voice and embrace the calm within you."
    },
    "Overwhelmed": {
        "name": "The Hanged Man",
        "description": "The Hanged Man represents letting go, surrender, and a shift in perspective.",
        "advice": "Take a step back, pause, and allow yourself to see things differently."
    },
    "Passionate": {
        "name": "The Lovers",
        "description": "The Lovers symbolize love, connection, and harmony.",
        "advice": "Follow your heart and embrace the deep connections in your life."
    },
    "Resilient": {
        "name": "Strength",
        "description": "The Strength card represents courage, patience, and inner power.",
        "advice": "Draw upon your inner strength to overcome challenges and persevere."
    }
    }

    return tarot_map.get(mood, {
        "name": "The Fool",
        "description": "The Fool represents new beginnings, spontaneity, and a free spirit.",
        "advice": "Take a leap of faith and embrace the unknown."
    })

def generate_image_prompt(tarot_card):
    # Construct a DALL·E prompt
    return f"""Generate a tarot card image titled '{tarot_card['name']}'. {tarot_card['description']} "A tarot card illustration in classic Rider-Waite style, featuring 'The Moon'. The card shows a large glowing moon with a human face in a serene night sky, two towers on the horizon, and a wolf and a dog howling at the moon. Below them, a river with a lobster crawling out. The scene is detailed, symbolic, and rendered in a hand-drawn vintage tarot art style with muted, earthy tones."""

def generate_tarot_image(prompt):
    # Call DALL·E to create an image
    response = client.images.generate(prompt=prompt,
    n=1,
    size="1024x1024")
    return response.data[0].url

# Main function
def tarot_mood_to_image(mood):
    # Step 1: Map mood to tarot card
    tarot_card = mood_to_tarot_mapping(mood)

    # Step 2: Generate image prompt
    image_prompt = generate_image_prompt(tarot_card)

    # Step 3: Generate image using DALL·E
    image_url = generate_tarot_image(image_prompt)

    # Step 4: Return JSON-compliant result
    return {
        "mood": mood,
        "tarotPrediction": tarot_card,
        "imagePrompt": image_prompt,
        "dalleImageUrl": image_url
    }

# Example Usage
result = tarot_mood_to_image("Resilient")
print(json.dumps(result, indent=2))
