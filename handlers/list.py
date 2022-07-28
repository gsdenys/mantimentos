from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
# from telegram.ext import CallbackContext

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

import prettytable as pt

from handlers.commons import cancel, restricted
from database import DBHelper


LIST, ALL, LACKING, WARNING = range(4)

options = ['Todos', 'Alerta', 'Faltando']

@restricted
def list(update: Update, context: CallbackContext) -> int:
    """Command to start the list conversation

    Args:
        update (Update): the incoming update
        context (CallbackContext): the telegram.ext.Handler callback

    Returns:
        int: representation of step to be handlered
    """
    reply_keyboard = [options]
    
    update.message.reply_text(
        f"Oi {update.message.chat.first_name.title()}, vamos lá,\n"
        "Esta funcionalide permite que vc liste todos os itens, os que estão faltando, "
        "ou que estão em alerta.\n"
        "Qual lista vc quer ver?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, 
            one_time_keyboard=True, 
            input_field_placeholder='Alerta, Faltando, ou Todos?'
        ),
    )
    
    return LIST

@restricted
def itens(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    table = pt.PrettyTable(['Item', 'Status'])
    table.align['Item'] = 'l'
    table.align['Status'] = 'r'

    data = []

    if (update.message.text == options[0]):
        data = DBHelper().get_items()
    else:
        data = DBHelper().get_items_by_status(options.index(update.message.text))
    
    STATUS = ["OK", "ALERTA", "EM FALTA"]

    for id, desc, status in data:
        table.add_row([desc.title(), STATUS[status]])

    update.message.reply_text(
        f'<pre>{table}</pre>', parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


# Add conversation handler
conversation = ConversationHandler(
    entry_points=[CommandHandler('lista', list)],
    states={
        LIST: [MessageHandler(Filters.regex('^(Todos|Alerta|Faltando)$'), itens)], 
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)