import jdatetime
import requests , pickle
from bs4 import BeautifulSoup
from telegram import InlineKeyboardButton
from utilities import *
from bs4_utils import *
from cache_utils import *
import hashlib
import threading
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
           "Host": "dining.fanap.ir",
           "Referer": "https://dining.fanap.ir/login/",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}

lunch_url = ""

current_csrf = ""

reservation_state = {}
reservation_choices = {}


def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)


def load_cookies(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        authenticate()


def authenticate(username="p.shalbafan", password="fanap1234"):
    r1 = requests.get("https://dining.fanap.ir/login/", headers=headers)
    soup = BeautifulSoup(r1.text, 'lxml')
    csrf = get_new_csrf(soup)
    r2 = requests.post(url = "https://dining.fanap.ir/login/check/", data={"csrfmiddlewaretoken":csrf, "username":username, "pass":password}, cookies=r1.cookies,
                       headers=headers, allow_redirects=False)
    save_cookies(r2.cookies, "cookies")


def reserve_lunch(key , food, drink="delete", csrfmiddlewaretoken=current_csrf, restur="فناپ ۳"):
    csrfmiddlewaretoken= current_csrf
    data = locals()
    print(data,lunch_url)
    result = requests.post(lunch_url,data=data,cookies=load_cookies("cookies"), headers=headers)
    if result.status_code == 403:
        authenticate()
        reserve_lunch(key,food,drink,csrfmiddlewaretoken,restur)
    return result


def get_lunch_response():
    global lunch_url
    result = requests.get("https://dining.fanap.ir/reservation/lunch", cookies=load_cookies("cookies"), headers=headers, allow_redirects=True)
    lunch_url = result.url
    if result.status_code in [404, 403]:
        authenticate()
        get_lunch_response()
        return
    return result


def get_new_csrf(souped_text):
    return souped_text.find("input", {"name": "csrfmiddlewaretoken"})["value"]


def process_status(result, date_goal):
    print(result[date_goal])
    exit(0)
    soup = BeautifulSoup(result.text, "lxml")
    global current_csrf
    global reservation_state
    global reservation_choices
    current_csrf = get_new_csrf(soup)
    re2 = soup.find_all("div", {"class": "card frm"})
    keyboard=[]
    for item in re2:
        if "disabled" in str(item):
            continue
        else:
            key = item.find("input", {"name": "key"})
            reservation = item.find_all("p", {"id": "text"})
            if len(reservation) == 1:
                your_food = reservation[0]
                your_food = your_food.string.split(":")[1]
                reservation_state[key["value"]] = {"food":your_food,"drink":"delete"}
            elif len(reservation) == 2:
                your_food, your_drink = reservation
                your_food = your_food.string.split(":")[1]
                your_drink = your_drink.string.split(":")[1]
                reservation_state[key["value"]] = {"food":your_food,"drink":your_drink}

            elif len(reservation) == 0:
                pass

            food_options = item.find("select", {"id": "f"}).find_all("option")
            drink_options = item.find("select", {"name": "drink"}).find_all("option")
            if key["value"] == date_goal:

                foods = []
                for option in food_options:
                    if option["value"] != "delete":
                        if option["value"] in (your_food):
                            foods.append(InlineKeyboardButton(" ✅  "+option["value"], callback_data="f:"+key["value"]+":" + "sdf"))
                        else:
                            foods.append(InlineKeyboardButton(option["value"], callback_data="f:"+key["value"]+":"+"sdfsd"))

                drinks=[]
                for option in drink_options:
                    if option["value"] != "delete":
                        if option["value"] in (your_drink):
                            drinks.append(InlineKeyboardButton(" ✅  "+option["value"], callback_data="d:"+key["value"]+":"+option["value"]))
                        else:
                            drinks.append(InlineKeyboardButton(option["value"], callback_data="d:"+key["value"]+":"+option["value"]))

                keyboard.append(foods)
                keyboard.append(drinks)
                keyboard.append([InlineKeyboardButton(" روز قبل ⬅", callback_data="t:"+previous_day(key["value"])),
                                 InlineKeyboardButton("➡️  روز بعد", callback_data="t:"+next_day(key["value"]))])
    return keyboard


def fetch_foods(date):
    get_choices(get_lunch_response())
    exit(0)
    try:
        result = get_dic_from_cache("options_index")
    except TypeError as e:
        result = get_lunch_response()
        result = index_options(result)
    return process_status(result, date)


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
            else:
                pass
            if is_any_option_available(drink_options):
                options_index = index_stuff_on_date(options_index, drink_options, date_as_key, "drink")
            else:
                pass
    write_dic_to_cache("options_index", options_index)
    return options_index


def is_any_option_available(options):
    return len(options) > 1


def index_stuff_on_date(index, options, key, kind):
    if key not in index:
        index[key] = {}
    stuffs = []
    for stuff in options:
        if stuff["value"] != "delete":
            stuffs.append(stuff["value"])
    index[key][kind] = stuffs
    return index


def get_choices():
    choice_hash = get_key_from_cache("choice_hash")
    if choice_hash is None:
        result = get_lunch_response()
        return index_choices(result)
    elif choice_hash ==






def index_choices(response):
    soup = convert_to_soup(response)
    reservation = soup.find_all("p", {"id": "text"})
    choice_hash = hashlib.md5(str(reservation).encode("utf-8")).digest()
    write_key_to_cache("choice_hash", choice_hash)
    print(get_key_from_cache("choice_hash") == choice_hash)
