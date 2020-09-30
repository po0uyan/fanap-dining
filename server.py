import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from init import fetch_foods,reserve_lunch, process_status
from utilities import *
updater = Updater(token='1112526007:AAETkQ0zSGjj-f40z9TecWN2oNbTbVwS99c', use_context=True)
dispatcher = updater.dispatcher
current_date = get_today()


def start(update, context):
    global current_date
    current_date = get_today()
    keyboard = fetch_foods(current_date)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text='لطفا غذای مد نظر خود را انتخاب نمایید\n'+"\n تاریخ: "+get_proper_jalali_time(current_date)+"\n.",reply_markup=reply_markup)


def button(update, context):
    global current_date
    drink="delete"
    food="delete"
    query = update.callback_query
    query.answer()
    splited=query.data.split(":")

    if splited[0] == "t":
        date = splited[1]
        current_date = date
        keyboard = fetch_foods(date)
    elif splited[0] == "d":
        drink = splited[2]
        result = reserve_lunch(current_date, food, drink)
        keyboard = process_status(result,current_date)
    elif splited[0] == "f":
        food = splited[2]
        result = reserve_lunch(current_date, food, drink)
        keyboard = process_status(result,current_date)

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text='لطفا غذای مد نظر خود را انتخاب نمایید\n'+"\n تاریخ: "+get_proper_jalali_time(current_date)+"\n.",reply_markup=reply_markup)





start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
updater.dispatcher.add_handler(CallbackQueryHandler(button))
