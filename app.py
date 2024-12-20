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
    "My purpose is to act as your personal virtual assistant, offering suggestions for enlighten your mindfulness.\n\n"
    'If you have any feature requests, feel free to email us'
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


# async def card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Prompt the user for their input to reveal a tarot card."""
#     await update.message.reply_text(
#         "🎴 You've chosen to reveal your card of the day!\n\n"
#         "Before we proceed, can you share your thoughts or expectations about today?"
#     )
#     context.user_data["awaiting_thoughts"] = True  # Set a flag for the next input


async def card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prompt the user for their input to reveal a tarot card."""
    user_id = update.effective_user.id
    no_of_reveal = context.bot_data.get("no_of_reveal", 0)

    # Check if the card has already been revealed
    if no_of_reveal >= 1:
        # Send a pop-up confirmation with inline buttons
        keyboard = [
            [
                InlineKeyboardButton("Yes, proceed!", callback_data="proceed"),
                InlineKeyboardButton("No, cancel", callback_data="cancel"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🎴 You've already revealed your card of the day! Do you want to proceed anyway?",
            reply_markup=reply_markup,
        )
        return

    # Prompt the user to share their thoughts
    await update.message.reply_text(
        "🎴 You've chosen to reveal your card of the day!\n\n"
        "Before we proceed, can you share your thoughts or expectations about today?"
    )
    context.user_data["awaiting_thoughts"] = True  # Set a flag for the next input


async def handle_thoughts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process the user's thoughts and continue chatting until the response is not chit-chat."""
    user_thought = update.message.text.strip()
    continue_conversation = True  # Flag to control the loop

    while continue_conversation:
        # Analyze the user input
        response = await analyze_user_input(user_thought)

        if "error" in response:
            await update.message.reply_text(response["error"])
            return

        answer_type = response.get("answer_type")
        response_content = response.get("response", {})

        if answer_type == "chit-chat":
            # Respond to chit-chat and prompt the user for more input
            text = response_content.get("text", "Let's chat!")
            await update.message.reply_text(text)
            return

        elif answer_type == "card":
            # Handle tarot card response
            image_link = response_content.get("image_link", DEFAULT_CARD_IMAGE)
            reading_response = response_content.get("text")
            await update.message.reply_text(f"✨ Here's your card of the day!\n\n")
            await update.message.reply_animation(animation=image_link)
            await update.message.reply_text(
                f"✨ Here's the prediction of the day\n\n{reading_response}"
            )
            continue_conversation = False  # Stop the loop
            context.bot_data["no_of_reveal"] += 1
            logger.info(f"Global no_of_reveal counter updated to {context.bot_data['no_of_reveal']}.")

        elif answer_type == "meme":
            # Handle meme response
            image_link = response_content.get("image_link", DEFAULT_MEME_IMAGE)
            await update.message.reply_animation(animation=image_link)
            continue_conversation = False  # Stop the loop

        else:
            # Handle unexpected response types
            await update.message.reply_text(
                "I'm not sure how to respond to that. Could you please elaborate?"
            )
            continue_conversation = False  # Stop the loop

async def handle_confirmation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user confirmation from inline keyboard buttons."""
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    if query.data == "proceed":
        # User chooses to proceed
        await query.edit_message_text(
            text="🎴 Proceeding to reveal your card of the day!\n\n"
                 "Before we proceed, can you share your thoughts or expectations about today?"
        )
        context.bot_data["no_of_reveal"] += 1  # Increment the counter
        context.user_data["awaiting_thoughts"] = True  # Set a flag for the next input

    elif query.data == "cancel":
        # User cancels the action
        await query.edit_message_text(text="🎴 No worries! Come back tomorrow for another reading.")


def main() -> None:
    """Run the bot."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.bot_data["no_of_reveal"] = 0

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("aboutme", aboutme))
    application.add_handler(CommandHandler("card", card))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_thoughts)
    )
    application.add_handler(CallbackQueryHandler(handle_confirmation_callback)) 

    application.run_polling()


if __name__ == "__main__":
    main()
