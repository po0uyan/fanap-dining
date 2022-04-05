from telegram import InlineKeyboardButton
from InvalidDateTimeProvided import InvalidDateTimeProvidedException
from utilities import previous_day, next_day


def prepare_inline_button_for_choices(result, date_goal):
    try:
        result = result[date_goal]
    except Exception as e:
        raise InvalidDateTimeProvidedException() from None
    foods = result["food"]
    drinks = result["drink"]
    keyboard = prepare_foods_choices_keyboard(foods,date_goal)
    keyboard.append(prepare_drinks_choices_keyboard(drinks,date_goal))
    keyboard.append(prepare_date_menu(date_goal))
    keyboard.append([InlineKeyboardButton("چشم‌انداز 📉" , callback_data="overview")])
    return keyboard



def prepare_foods_choices_keyboard(stuff,date):
    keyboard = []
    checked = " ✅  "
    for index, key in enumerate(stuff):
        callback_key = "f" + ":" + date + ":" + str(index)
        if stuff[key]:
            keyboard.append([InlineKeyboardButton(checked + key, callback_data=callback_key)])
        else:
            keyboard.append([InlineKeyboardButton(key, callback_data=callback_key)])
    return keyboard


def prepare_drinks_choices_keyboard(stuff,date):
    keyboard = []
    checked = " ✅  "
    for index, key in enumerate(stuff):
        callback_key = "d" + ":" + date + ":" + str(index)
        if stuff[key]:
            keyboard.append(InlineKeyboardButton(checked + key, callback_data=callback_key))

        else:
            keyboard.append(InlineKeyboardButton(key, callback_data=callback_key))
    return keyboard


def prepare_date_menu(date):
    yesterday = " روز قبل ⬅"
    tomorrow = "➡️  روز بعد"
    yesterday_date = previous_day(date)
    tomorrow_date = next_day(date)
    keyboard = [InlineKeyboardButton(yesterday, callback_data="t:"+yesterday_date), InlineKeyboardButton(tomorrow, callback_data="t:"+tomorrow_date)]
    return keyboard