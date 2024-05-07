from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters)
import logging
import nest_asyncio
import asyncio
import json
import os
import itertools

# Replace this with your actual token
TELEGRAM_BOT_TOKEN = "70050"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Conversation states
NAME, PHONE, LANGUAGE = range(3)
UNSUBSCRIBE_PHONE = range(1)

# Path to JSON file storing subscriptions
SUBSCRIPTIONS_FILE = "subscribers.json"

# Default JSON structure
DEFAULT_STRUCTURE = {"_default": {}}

# Language codes mapping
LANGUAGE_CODES = {
    'English': 'en',
    'Hebrew': 'iw',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Russian': 'ru',
    'Arabic': 'ar',
    'Chinese': 'zh-TW',
    'Portuguese': 'pt',
    'Japanese': 'ja',
    'Korean': 'ko'
}

def load_subscriptions() -> dict:
    """Load subscriptions from the JSON file."""
    if os.path.exists(SUBSCRIPTIONS_FILE):
        with open(SUBSCRIPTIONS_FILE, "r") as file:
            return json.load(file)
    else:
        return DEFAULT_STRUCTURE


def save_subscriptions(data: dict) -> None:
    """Save subscriptions to the JSON file."""
    with open(SUBSCRIPTIONS_FILE, "w") as file:
        json.dump(data, file, indent=4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message, preview of the message of the day, and prompt to subscribe."""
    # Example preview of the message of the day
    preview_message = (
        "🌟 *Message of the Day Preview* 🌟\n\n"
        "Here's a preview of what you'll receive:\n\n"
        "*📸 Picture of the Day:*\n"
        "_Picture description_\n\n"
        "*💡 Interesting Facts:*\n"
        "Did you know...\n\n"
        "*📜 Today in History:*\n"
        "On this day...\n\n"
        "*🐾 Animal Facts:*\n"
        "Fascinating fact about animals...\n\n"
        "*📖 Random Wikipedia Summary:*\n"
        "Summary of a random Wikipedia article...\n\n"
        "*😂 Joke of the Day:*\n"
        "Hilarious joke...\n\n"
        "*Enjoy your day and keep learning!*"
    )

    # Keyboard to prompt for subscription
    keyboard = [[KeyboardButton("📋 Subscribe")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        f"👋 Welcome to the subscription bot!\n\n{preview_message}\n\n"
        "You want to receive Message of the Day to your WhatsApp once a day to expand your knowledge and start your day with a smile?\n"
        "Press 'Subscribe' to start receiving daily messages!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the conversation to subscribe a user to the daily message."""
    await update.message.reply_text("📋 Please provide your full name:")
    return NAME


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive the user's name and prompt for phone number."""
    context.user_data['name'] = update.message.text

    # Keyboard to share phone number
    keyboard = [[KeyboardButton("📞 Share Phone Number", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("☎️ Now, please share your phone number or type it manually (e.g., +97252000000):", reply_markup=reply_markup)
    return PHONE


async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive the user's phone number and prompt for language preference."""
    message = update.message
    if message.contact:
        # Received phone number via contact sharing
        phone_number = "whatsapp:" + message.contact.phone_number
    else:
        # Received phone number via manual entry
        phone_number = "whatsapp:" + message.text

    context.user_data['phone'] = phone_number

    # Language options
    keyboard = [['English', 'Hebrew', 'Spanish'], ['French', 'German', 'Italian'], ['Russian', 'Arabic', 'Chinese'],
                ['Portuguese', 'Japanese', 'Korean']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("🌐 Please select your preferred language:", reply_markup=reply_markup)
    return LANGUAGE


async def receive_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive the user's preferred language and save the subscription details."""
    language_name = update.message.text
    context.user_data['language'] = LANGUAGE_CODES.get(language_name, 'en')  # Default to 'en' if not found
    name = context.user_data['name']
    phone = context.user_data['phone']
    language = context.user_data['language']

    # Load existing subscriptions
    subscriptions = load_subscriptions()

    # Counter for generating unique subscription IDs
    subscription_id_counter = itertools.count(1)

    # Generate a unique subscription ID
    subscriber_id = next(subscription_id_counter)

    # Add the new subscription
    subscriptions["_default"][subscriber_id] = {
    "phone_number": phone,
    "name": name,
    "language": language    
}

    # Save subscriptions to file
    save_subscriptions(subscriptions)

    # WhatsApp message link
    whatsapp_link = "https://wa.me/14155238886?text=join+spend-wing"

    await update.message.reply_text(
        f"✅ Thank you {name}, you've been subscribed with phone number: {phone} and language preference: {language}.\n\n"
        f"➡️ Click [here]({whatsapp_link}) to send a WhatsApp message to Twilio and receive the Message of the Day.",
        parse_mode='Markdown', disable_web_page_preview=True
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cancel the conversation."""
    await update.message.reply_text("🚫 Subscription process cancelled.")
    return ConversationHandler.END


async def request_unsubscribe_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Request the user's phone number to unsubscribe them."""
    keyboard = [[KeyboardButton("📞 Share Phone Number", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("☎️ Please share your phone number to unsubscribe or type it manually (e.g., +97200000000):", reply_markup=reply_markup)
    return UNSUBSCRIBE_PHONE


async def unsubscribe_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unsubscribe a user from the daily message based on their phone number."""
    message = update.message
    if message.contact:
        # Received phone number via contact sharing
        phone_number = "whatsapp:" + message.contact.phone_number
    else:
        # Received phone number via manual entry
        phone_number = "whatsapp:" + message.text

    # Load existing subscriptions
    subscriptions = load_subscriptions()
    default_subscriptions = subscriptions["_default"]

    # Find and remove the user
    to_remove = None
    for user_id, data in default_subscriptions.items():
        if data.get("phone_number") == phone_number:
            to_remove = user_id
            break

    if to_remove:
        del default_subscriptions[to_remove]
        save_subscriptions(subscriptions)
        await update.message.reply_text("🚫 You've been unsubscribed from daily messages!")
    else:
        await update.message.reply_text("❌ Could not find your subscription. Please ensure you've shared or typed the correct phone number.")

    return ConversationHandler.END


async def main():
    """Start the bot."""
    # Create the Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Create subscription conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("subscribe", subscribe)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
            PHONE: [MessageHandler(filters.CONTACT | filters.TEXT & ~filters.COMMAND, receive_phone)],
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_language)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # Create unsubscribe conversation handler
    unsubscribe_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("unsubscribe", request_unsubscribe_phone)],
        states={
            UNSUBSCRIBE_PHONE: [MessageHandler(filters.CONTACT | filters.TEXT & ~filters.COMMAND, unsubscribe_phone)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(unsubscribe_conv_handler)

    # Start the bot
    await application.run_polling()


if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
