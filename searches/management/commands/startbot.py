import os

from django.core.management.base import BaseCommand, CommandError

from searches.models import TelegramUser
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove

from searches.models import SearchArea, SearchRequest, TelegramUser

def start(update:Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton('Search', callback_data='search')],
        [InlineKeyboardButton('History', callback_data='history')],
    ]

    reply_markup=InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Hello!", reply_markup=reply_markup)

    user = update.message.from_user
    obj, created = TelegramUser.objects.get_or_create(
        telegram_id=user.id,
        telegram_name=user.username
    )
    return "BUTTON"


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = query.from_user
    query.answer()
    if query.data == 'history':
        text = "Search history: \n" + "\n".join(SearchRequest.objects.filter(user__id = user.id))
        query.edit_message_text(text=text)
    elif query.data == 'search':
        query.edit_message_text("Please enter search request")
        return "SEARCH"


def cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def search(update: Update, context: CallbackContext) -> None:
    user = TelegramUser.objects.get(telegram_id=update.message.from_user.id)
    SearchRequest.create(user=user, request=update.message.text)


class Command(BaseCommand):
    help = 'Starts obt the specified poll for voting'

    def handle(self, *args, **options):
        
        token = os.environ['TELEGRAM_TOKEN']
        updater = Updater(token)
        
        dispatcher = updater.dispatcher

        # I know pass_user_data is deprecated, but... I'm lazy to find better solution
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                "BUTTON": [CallbackQueryHandler(button, pass_user_data=True)],
                "SEARCH": [MessageHandler(Filters._All, search)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )
        dispatcher.add_handler(conv_handler)
 
        updater.start_polling()
        updater.idle()
