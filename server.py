from telegram import InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from init import fetch_options_for_date, prepare_inline_button_for_choices, check_user
from init import reserve_inline
from utilities import *
updater = Updater(token='1112526007:AAETkQ0zSGjj-f40z9TecWN2oNbTbVwS99c', use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    check_user(update)
    key = get_today()

    keyboard = fetch_options_for_date(get_today())

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text='لطفا غذای مد نظر خود را انتخاب نمایید\n' +"\n تاریخ: " + get_proper_jalali_time(key) + "\n.", reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    splited=query.data.split(":")
    key = get_today()

    if splited[0] == "t":
        key = splited[1]
        keyboard = fetch_options_for_date(key)
    elif splited[0] == "d":
        key = splited[1]
        drink = splited[2]
        result = reserve_inline(key, drink, "drink")
        if result is None:
            query.answer(text='لطفا نوشیدنی را پس از انتخاب غذا، انتخاب نمایید', show_alert=True)
            return
        keyboard = prepare_inline_button_for_choices(result, key)
    elif splited[0] == "f":
        key = splited[1]
        food = splited[2]
        result = reserve_inline(key, food, "food")
        keyboard = prepare_inline_button_for_choices(result, key)

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text='لطفا غذای مد نظر خود را انتخاب نمایید\n' +"\n تاریخ: " + get_proper_jalali_time(key) + "\n.", reply_markup=reply_markup)





start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
updater.dispatcher.add_handler(CallbackQueryHandler(button))
