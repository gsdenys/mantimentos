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

ALERT, SELECT = range(2)

@restricted
def falta(update: Update, context: CallbackContext) -> int:
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
            "Digite o __Nome do Item__ para marca-lo como *EM FALTA*, ou"
            "para cancelar digite /cancel",
            parse_mode='MarkdownV2'
    )
        
    return ALERT
    
@restricted
def select(update: Update, context: CallbackContext) -> int:
    """Handler to insert itens to the list

    Args:
        update (Update): the incoming update
        context (CallbackContext): the telegram.ext.Handler callback

    Returns:
        int: representation of step to be handlered
    """
    FLAG_FALTA = 2
    item = update.message.text
    resp = DBHelper().update_item_by_Name(item, FLAG_FALTA)
    
    if resp:
        update.message.reply_text(
            f"O item __{item}__ foi marcado com *EM ALERTA*",
            parse_mode='MarkdownV2'
        )
    else:
        update.message.reply_text(
            f"__{item}:__  item *NÃO ENCONTRADO*",
            parse_mode='MarkdownV2'
        )
    
    return ConversationHandler.END

# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
conversation = ConversationHandler(
    entry_points=[CommandHandler('alerta', falta)],
    states={
        ALERT: [MessageHandler(Filters.text & ~Filters.command, select)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
