from telegram import Update
# from telegram.ext import CallbackContext

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

from handlers.commons import cancel
from database import DBHelper

import re

ITEMS, MORE = range(2)

def new(update: Update, context: CallbackContext) -> int:
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
            "Digite a __lista de itens__ para inserir no controle de mantimentos, "
            "ou /cancel para cancelar",
            parse_mode='MarkdownV2'
    )
        
    return ITEMS
    
def new_item(update: Update, context: CallbackContext) -> int:
    """Handler to insert itens to the list

    Args:
        update (Update): the incoming update
        context (CallbackContext): the telegram.ext.Handler callback

    Returns:
        int: representation of step to be handlered
    """
    items = re.split(',|\n|;',update.message.text)
    
    for item in items:
        DBHelper().add_item(item)

    if len(items) > 1:
        update.message.reply_text(
            f"Os itens *{items}* foram inseridos com sucesso!",
             parse_mode='MarkdownV2'
        )
    else:
        update.message.reply_text(
            f"O item *{items[0]}* foi inseridos com sucesso!",
             parse_mode='MarkdownV2'
        )
        
    update.message.reply_text("Digite os novos itens ou /cancel para cancelar.")
    
    return ITEMS


# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
conversation = ConversationHandler(
    entry_points=[CommandHandler('new', new)],
    states={
        ITEMS: [MessageHandler(Filters.text & ~Filters.command, new_item)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
