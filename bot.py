import logging
import os

from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
)

from database import DBHelper

from handlers.items import conversation as items_handler
from handlers.list import conversation as list_handler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '443'))
APP = os.getenv("APP")

LIST_OF_ADMINS = os.getenv("LIST_OF_ADMINS").split(",")

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    # reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?'
    )


def main() -> None:
    """Run the bot."""
    DBHelper().setup()
    
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(items_handler)
    dispatcher.add_handler(list_handler)

    # Start the Bot
    # updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


     # Start the Bot
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=os.getenv("TELEGRAM_TOKEN"),
        webhook_url=APP + os.getenv("TELEGRAM_TOKEN")
    )


if __name__ == '__main__':
    main()