from select import select
from telegram import Update
# from telegram.ext import CallbackContext

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

from handlers.commons import cancel, restricted
from database import DBHelper

import re

ALERT, SELECT, = range(2)

@restricted
def alert(update: Update, context: CallbackContext) -> int:
    """Command to start the insert itens flow

    Args:
        update (Update): the incoming update
        context (CallbackContext): the telegram.ext.Handler callback

    Returns:
        int: representation of step to be handlered
    """
    name = update.message.chat.first_name.title()
    
    update.message.reply_text(
            f"Oi *{name}*, vamos lá,\n"
            "Digite o __Nome do Item__ para inserir um alerta de quantidade, ou"
            "para cancelar digite /cancel",
            parse_mode='MarkdownV2'
    )
        
    return ALERT
    
@restricted
def SELECT(update: Update, context: CallbackContext) -> int:
    """Handler to insert itens to the list

    Args:
        update (Update): the incoming update
        context (CallbackContext): the telegram.ext.Handler callback

    Returns:
        int: representation of step to be handlered
    """

    update.message.reply_text(update.message.text)
    
    return ConversationHandler.END



# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
conversation = ConversationHandler(
    entry_points=[CommandHandler('alerta', alert)],
    states={
        ALERT: [MessageHandler(Filters.text & ~Filters.command, select)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
