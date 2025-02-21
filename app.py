import os
import logging
from datetime import datetime
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)
from prompt import analyze_user_input, DEFAULT_CARD_IMAGE, DEFAULT_MEME_IMAGE
from prefect import flow, task

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
    "I am a Telegram bot developed by BT\n\n"
    "My purpose is to act as your personal virtual assistant, offering suggestions for enlightening your mindfulness.\n\n"
    'If you have any feature requests, feel free to email us at '
    '<a href="mailto:supakavadee.r@gmail.com">supakavadee.r@gmail.com</a>.'
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    first_name = update.effective_user.first_name or "there"
    welcome_message = WELCOME_MESSAGE.format(first_name=first_name)

    keyboard = [[KeyboardButton("/card")], [KeyboardButton("/aboutme")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    await update.message.reply_html(welcome_message, reply_markup=reply_markup)


async def aboutme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Describe the bot's functionality."""
    await update.message.reply_html(ABOUT_ME_TEXT)


async def card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ensure only one tarot card per user per day, but allow chatting afterward."""
    user_id = update.effective_user.id
    today_date = datetime.now().strftime("%Y-%m-%d")

    last_reveal_date = context.user_data.get("last_reveal_date")

    if last_reveal_date == today_date:
        await update.message.reply_text("🎴 You've already revealed your card today! Feel free to chat.")
        return

    await update.message.reply_text(
        "🎴 You've chosen to reveal your card of the day!\n\n"
        "Before we proceed, can you share your thoughts or expectations about today?"
    )
    context.user_data["awaiting_thoughts"] = True


async def handle_thoughts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user input, ensuring only one card per day while allowing free chatting."""
    user_id = update.effective_user.id
    today_date = datetime.now().strftime("%Y-%m-%d")

    user_thought = update.message.text.strip()
    response = await analyze_user_input(user_thought)

    if "error" in response:
        await update.message.reply_text(response["error"])
        return

    answer_type = response.get("answer_type")
    response_content = response.get("response", {})

    # ✅ Prevent OpenAI from giving another tarot card if user already got one
    last_reveal_date = context.user_data.get("last_reveal_date")
    if last_reveal_date == today_date and answer_type == "card":
        answer_type = "chit-chat"  # Force chit-chat mode
        response_content["text"] = response_content.get("text", "Let's chat!")

    if answer_type == "card":
        image_link = response_content.get("image_link", DEFAULT_CARD_IMAGE)
        reading_response = response_content.get("text")

        await update.message.reply_text(f"✨ Here's your card of the day!\n\n")
        await update.message.reply_animation(animation=image_link)
        await update.message.reply_text(f"✨ Prediction for today:\n\n{reading_response}")

        # ✅ Store last reveal date to block multiple tarot cards per day
        context.user_data["last_reveal_date"] = today_date

    elif answer_type == "chit-chat":
        await update.message.reply_text(response_content.get("text", "Let's chat!"))

    elif answer_type == "meme":
        image_link = response_content.get("image_link", DEFAULT_MEME_IMAGE)
        await update.message.reply_animation(animation=image_link)

    else:
        await update.message.reply_text("I'm not sure how to respond. Can you rephrase?")

async def handle_confirmation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user confirmation from inline keyboard buttons."""
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    if query.data == "proceed":
        await query.edit_message_text(
            text="🎴 Proceeding to reveal your card of the day!\n\n"
                 "Before we proceed, can you share your thoughts or expectations about today?"
        )
        context.user_data["awaiting_thoughts"] = True

    elif query.data == "cancel":
        await query.edit_message_text(text="🎴 No worries! Come back tomorrow for another reading.")


def main() -> None:
    print("Bot is starting...")  # Debugging
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add more logging
    print("Adding handlers...")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("aboutme", aboutme))
    application.add_handler(CommandHandler("card", card))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_thoughts))
    application.add_handler(CallbackQueryHandler(handle_confirmation_callback))

    print("Starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES, timeout=10, poll_interval=1)

    print("Polling stopped!")  # If this prints, polling failed


if __name__ == "__main__":
    main()
