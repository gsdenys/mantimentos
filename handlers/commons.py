from asyncio.log import logger
from functools import wraps
import logging
import os
from telegram import ReplyKeyboardRemove, Update

from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)

LIST_OF_ADMINS = os.getenv("LIST_OF_ADMINS").split(",")


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! Espero que tenha um excelente dia.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def restricted(func):
    logger.info("entrou")
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        logging.error(user_id)
        if user_id not in LIST_OF_ADMINS:
            fname = update.effective_user.first_name
            lname = update.effective_user.last_name
            
            user = f"{fname} {lname}"
            
            logging.error(f"Authorization denied for {user} ({user_id})")
            
            update.message.reply_text(f"Olá {fname} {lname}!")
            update.message.reply_text("Lamento informar, mas sou um BOT de acesso restrito e não posso falar contigo.")
            update.message.reply_text("Ainda assim, caso queira me usar, sou de codigo aberto e podes me encontrar em:")
            update.message.reply_text("Au revoir")
            
            return
        return func(update, context, *args, **kwargs)
    return wrapped