from redis import Redis
from keyboard_utils import prepare_inline_button_for_choices
from cache_utils import *
import request_utils
from rq import Queue
import repository
import ast

q = Queue(connection=Redis())


def fetch_options_for_date(date):
    result = repository.fetch_options_from_repo()
    return prepare_inline_button_for_choices(result, date)


def index_options(response):
    options_index = {}
    soup = convert_to_soup(response)
    food_cards = soup.find_all("div", {"class": "card frm"})
    for card in food_cards:
        if "disabled" in str(card):
            continue
        else:
            date_as_key = card.find("input", {"name": "key"})["value"]
            date_as_key = str(date_as_key)
            food_options = card.find("select", {"id": "f"}).find_all("option")
            drink_options = card.find("select", {"name": "drink"}).find_all("option")
            if is_any_option_available(food_options):
                options_index = index_stuff_on_date(options_index, food_options, date_as_key, "food")

            if is_any_option_available(drink_options):
                options_index = index_stuff_on_date(options_index, drink_options, date_as_key, "drink")

            options_index = add_choice_to_index(options_index, card,date_as_key)

    write_dic_to_cache("options_index", options_index)
    return options_index


def is_any_option_available(options):
    return len(options) > 1


def index_stuff_on_date(index, options, key, kind):
    if key not in index:
        index[key] = {}
    stuffs = {}
    for stuff in options:
        if stuff["value"] != "delete":
            stuffs[stuff["value"]] = 0
    index[key][kind] = stuffs
    return index


def add_choice_to_index(index, card, key):
    choices = card.find_all("p", {"id": "text"})
    if(choices):
        food , drink = choices
        food = prepare_option(food.text)
        drink = prepare_option(drink.text)
        index[key] = change_index_option(index[key],food,"food")
        index[key] = change_index_option(index[key],drink,"drink")
    return index


def change_index_option(index,option,kind):
    if option in index[kind]:
        index[kind][option] = 1
    return index

def prepare_option(option):
    return option.split(":")[1].strip()




def reserve_inline(date , stuff_index, type, restur="فناپ ۳"):
    options = repository.fetch_options_from_repo()
    result = options[date][type]
    for index, key in enumerate(result):
        if str(index)==str(stuff_index):
            if result[key] == 1:
                options[date][type][key] = 0
                options[date] = if_food_remove_all_drinks(options[date], type)
            else:

                if if_there_is_a_food(options[date]):
                    options[date][type][key] = 1
                elif type == "food":
                    options[date][type][key] = 1
                else:
                    return
            q.enqueue(request_utils.reserve_lunch,date,options[date],restur)
        else:
            options[date][type][key] = 0
    write_dic_to_cache("options_index", options)
    return options



def if_food_remove_all_drinks(options,type):
    if type == "food":
        for key in options["drink"]:
            options["drink"][key] = 0
    return options

def if_there_is_a_food(options):
    for key in options["food"]:
        if options["food"][key] == 1:
            return True
    return False


def check_user(update):
    try:
        print(get_dic_from_cache(update.message.chat.id))
    except Exception as e:
        print(e)
        update.message.reply_text(text="slm login kon")
    write_dic_to_cache(update.message.chat.id,ast.literal_eval(str(update)))