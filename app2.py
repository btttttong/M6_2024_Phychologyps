import os
import logging
import aiohttp
from datetime import datetime
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from prompt import analyze_user_input, analyze_user_audio_input, DEFAULT_CARD_IMAGE, DEFAULT_MEME_IMAGE

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set in environment variables.")
    raise EnvironmentError("Missing BOT_TOKEN.")

VOICE_SAVE_PATH = "downloads"
os.makedirs(VOICE_SAVE_PATH, exist_ok=True)

WELCOME_MESSAGE = (
    "<b>🌟 Hey {first_name}! 🌟</b>\n\n"
    "I am <b>Gini 🧞‍♀️</b>, your virtual assistant.\n\n"
    "<b>Commands 🧞‍♀️</b>\n"
    "🔮  /card - Your tarot card of the day\n"
    "🤖  /aboutme - Learn about me!"
)

ABOUT_ME_TEXT = (
    "I am a Telegram bot developed by BT.\n"
    "I can read tarot cards and analyze your emotions from voice input.\n"
    "Email: <a href='mailto:supakavadee.r@gmail.com'>supakavadee.r@gmail.com</a>"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    first_name = update.effective_user.first_name or "there"
    welcome_message = WELCOME_MESSAGE.format(first_name=first_name)

    keyboard = [[KeyboardButton("/card")], [KeyboardButton("/aboutme")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_html(welcome_message, reply_markup=reply_markup)


async def aboutme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Describe the bot's functionality."""
    await update.message.reply_html(ABOUT_ME_TEXT)


async def card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initiate tarot card reading (only once per day)."""
    user_id = update.effective_user.id
    today_date = datetime.now().strftime("%Y-%m-%d")

    last_reveal_date = context.user_data.get("last_reveal_date")

    if last_reveal_date == today_date:
        await update.message.reply_text("🎴 You've already received a card today! Feel free to chat.")
        return

    await update.message.reply_text(
        "🎴 Share your thoughts before I reveal your tarot card!"
    )
    context.user_data["awaiting_thoughts"] = True


async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user text input for tarot cards or chit-chat."""
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    today_date = datetime.now().strftime("%Y-%m-%d")

    last_reveal_date = context.user_data.get("last_reveal_date")

    #   If the user already got a tarot card today, override the response to chit-chat.
    if last_reveal_date == today_date:
        response = {"answer_type": "chit-chat", "response": {"text": "Let's chat! What's on your mind?"}}
    elif "awaiting_thoughts" in context.user_data:
        #   Instead of chit-chat, immediately analyze user input for a tarot card
        response = await analyze_user_input(user_input)
        del context.user_data["awaiting_thoughts"]
    else:
        response = await analyze_user_input(user_input)

    if "error" in response:
        await update.message.reply_text(response["error"])
        return

    answer_type = response.get("answer_type")
    response_content = response.get("response", {})

    if answer_type == "card":
        image_link = response_content.get("image_link", DEFAULT_CARD_IMAGE)
        reading_response = response_content.get("text", "Here is your tarot reading.")

        await update.message.reply_photo(photo=image_link, caption=f"🔮 Prediction:\n{reading_response}")

        #   Store last reveal date to prevent multiple tarot cards
        context.user_data["last_reveal_date"] = today_date


    elif answer_type == "chit-chat":
        await update.message.reply_text(response_content.get("text", "Let's chat!"))

    elif answer_type == "meme":
        image_link = response_content.get("image_link", DEFAULT_MEME_IMAGE)

        # Check if the link is a valid GIF/MP4 (for animations)
        if image_link.endswith((".gif", ".mp4")):
            await update.message.reply_animation(animation=image_link)
        else:
            await update.message.reply_photo(photo=image_link, caption="Here's something fun for you! 😆")

    else:
        await update.message.reply_text("I'm not sure how to respond. Can you rephrase?")


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process voice messages for emotion analysis."""
    voice = update.message.voice
    file_id = voice.file_id
    file_path = os.path.join(VOICE_SAVE_PATH, f"{file_id}.oga")

    #   Download voice file from Telegram
    file = await context.bot.get_file(file_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(file.file_path) as resp:
            if resp.status == 200:
                with open(file_path, "wb") as f:
                    f.write(await resp.read())

    logger.info(f"Downloaded voice file: {file_path}")

    #   Convert .oga to .wav
    wav_path = file_path.replace(".oga", ".wav")
    conversion_cmd = f"ffmpeg -i {file_path} -ar 16000 -ac 1 {wav_path}"
    
    try:
        os.system(conversion_cmd)
        logger.info(f"Converted to WAV: {wav_path}")
    except Exception as e:
        logger.error(f"Error converting audio: {e}")
        await update.message.reply_text("⚠️ Error processing audio. Please try again.")
        return

    #   Analyze the audio
    response = await analyze_user_audio_input(wav_path)

    if "error" in response:
        await update.message.reply_text("⚠️ Error processing audio. Please try again.")
        return

    transcription = response.get("transcription", "I couldn't understand that.")
    emotion = response.get("emotion", {})
    depression_score = response.get("depression_score", 0.0)
    ai_response = response.get("ai_response", "Let's talk!")

    reply_message = (
        f"🎙 **Transcription:** {transcription}\n"
        f"😶 **Emotions:** {emotion}\n"
        f"📉 **Depression Score:** {depression_score:.2f}\n"
        f"🤖 **AI Response:** {ai_response}"
    )

    await update.message.reply_text(reply_message)


def main() -> None:
    """Run the Telegram bot."""
    print("Bot is starting...")
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    #   Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("aboutme", aboutme))
    application.add_handler(CommandHandler("card", card))

    #   Text & Voice Message Handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    print("Starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES, timeout=10, poll_interval=1)


if __name__ == "__main__":
    main()
