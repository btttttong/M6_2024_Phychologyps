import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from prompt import analyze_user_input, DEFAULT_CARD_IMAGE, DEFAULT_MEME_IMAGE

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set in environment variables.")
    raise EnvironmentError("Missing BOT_TOKEN.")

WELCOME_MESSAGE = (
    "<b>🌟 Hey {first_name}! 🌟</b>\n\n"
    "I am <b>Gini 🧞‍♀️</b>, your virtual assistant.\n\n"
    "<b>Commands 🧞‍♀️</b>\n"
    "You can control me by clicking any option below or sending these commands:\n\n"
    "🔮  /card - your card of the day\n"
    "🤖  /aboutme - describe the functionality of the bot"
)

ABOUT_ME_TEXT = (
    "I am a Telegram bot developed by Gino and BT under Anton Topchii's supervision.\n\n"
    "My purpose is to act as your personal virtual assistant, offering suggestions for exciting places to visit and must-see attractions in Thailand. "
    "Furthermore, I'm here to support you academically, providing aid and resources for your studies.\n\n"
    'If you have any feature requests, feel free to <a href="mailto:ginoasuncion@gmail.com">email us</a> at ginoasuncion@gmail.com or '
    '<a href="mailto:supakavadee.r@gmail.com">supakavadee.r@gmail.com</a>.'
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    first_name = update.effective_user.first_name or "there"
    welcome_message = WELCOME_MESSAGE.format(first_name=first_name)

    keyboard = [
        [KeyboardButton("/card")],
        [KeyboardButton("/aboutme")]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    await update.message.reply_html(welcome_message, reply_markup=reply_markup)


async def aboutme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Describe the bot's functionality."""
    await update.message.reply_html(ABOUT_ME_TEXT)


async def card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prompt the user for their input to reveal a tarot card."""
    await update.message.reply_text(
        "🎴 You've chosen to reveal your card of the day!\n\n"
        "Before we proceed, can you share your thoughts or expectations about today?"
    )
    context.user_data["awaiting_thoughts"] = True  # Set a flag for the next input


async def handle_thoughts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process the user's thoughts and interact with OpenAI."""
    if context.user_data.get("awaiting_thoughts"):
        user_thought = update.message.text.strip()
        context.user_data["awaiting_thoughts"] = False  # Reset flag

        # Call OpenAI handler to analyze the input
        response = await analyze_user_input(user_thought)

        if "error" in response:
            await update.message.reply_text(response["error"])
            return

        answer_type = response.get("answer_type")
        response_content = response.get("response", {})

        if answer_type == "card":
            image_link = response_content.get("image_link", DEFAULT_CARD_IMAGE)
            await update.message.reply_text(f"✨ Here's your card of the day!")
            await update.message.reply_animation(animation=image_link)
        elif answer_type == "chit-chat":
            text = response_content.get("text", "Let's chat!")
            await update.message.reply_text(text)
        elif answer_type == "meme":
            image_link = response_content.get("image_link", DEFAULT_MEME_IMAGE)
            await update.message.reply_animation(animation=image_link)
        else:
            await update.message.reply_text(
                "I'm not sure how to respond to that. Could you please elaborate?"
            )
    else:
        await update.message.reply_text(
            "Please use the /card command to start sharing your thoughts!"
        )


def main() -> None:
    """Run the bot."""
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("aboutme", aboutme))
    application.add_handler(CommandHandler("card", card))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_thoughts))

    application.run_polling()


if __name__ == "__main__":
    main()
