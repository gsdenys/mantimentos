from functools import wraps
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', '443'))
APP = os.getenv("APP")

LIST_OF_ADMINS = os.getenv("LIST_OF_ADMINS").split(",")


logging.info(os.getenv("TELEGRAM_TOKEN"))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN")

def restricted(func):
    logger.info("entrou")
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        logging.error(user_id)
        logging.error(LIST_OF_ADMINS)
        if user_id not in LIST_OF_ADMINS:
            
            fname = update.effective_user.first_name
            lname = update.effective_user.last_name
            
            user = f"{fname} {lname}"
            
            logging.error(f"Authorization denied for {user} ({user_id})")
            
            update.message.reply_text(f"Olá {fname} {lname}!")
            update.message.reply_text("Lamento informar, mas sou um BOT de acesso restrito e não posso falar contigo.")
            update.message.reply_text("Ainda assim, caso queira me usar, sou de codigo aberto e podes me encontrar em:")
            update.message.reply_text("https://github.com/gsdenys/mantimentos")
            update.message.reply_text("Au revoir")
            
            return
        return func(update, context, *args, **kwargs)
    return wrapped


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
@restricted
def start(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat_id
    first_name =update.message.chat.first_name
    # last_name = update.message.chat.last_name
    # username = update.message.chat.username
    # print("chat_id : {} and firstname : {} lastname : {}  username {}". format(chat_id, first_name, last_name , username))
    context.bot.send_message(chat_id, 'Ciao ' + first_name + 'text')


def help(update, context):
    """Send a message when the command /help is issued."""
    msg = "Sou um BOT par um controle de estoque de mantimetos familiar, e vc não deve fazer parte da familia."

    update.message.reply_text(msg)

@restricted
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
@restricted
def new(update, context):
    update.message.reply_text("Hello Command")


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    
    
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("new", new))


    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url=APP + TOKEN
    )

    # updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()