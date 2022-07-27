from asyncio.log import logger
from telegram import ReplyKeyboardRemove, Update

from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! Espero que tenha um excelente dia.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END