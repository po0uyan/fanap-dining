from redis import Redis
import requests , pickle
from cache_utils import *
from rq import Queue

import repository
q = Queue(connection=Redis())

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
           "Host": "dining.fanap.ir",
           "Referer": "https://dining.fanap.ir/login/",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}

lunch_url = ""

lunch_reserve_url = "https://dining.fanap.ir/reservation/lunch"
login_csrf_url = "https://dining.fanap.ir/login/"
login_url = "https://dining.fanap.ir/login/check/"


def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)


def load_cookies(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        authenticate()

def login_to_get_csrf():
    r1 = requests.get(login_csrf_url, headers=headers)
    soup = convert_to_soup(r1)
    return r1.cookies, get_new_csrf(soup)


def authenticate(username="p.shalbafan", password="fanap1234"):
    cookies, csrf = login_to_get_csrf()
    login_request = requests.post(url = login_url, data={"csrfmiddlewaretoken":csrf, "username":username, "pass":password}, cookies=cookies,
                       headers=headers, allow_redirects=False)
    save_cookies(login_request.cookies, "cookies")


def reserve_lunch(key ,options_for_date, restur="فناپ ۳"):
    result = get_lunch_response()
    data = {}
    data["restur"] = restur
    data["key"] = key
    data["food"] = get_choosed_option(options_for_date,"food")
    data["drink"] = get_choosed_option(options_for_date,"drink")
    data["csrfmiddlewaretoken"] = get_cached_csrf_token_for_user()
    print(data)
    result = requests.post(result.url,data=data,cookies=load_cookies("cookies"), headers=headers)
    if result.status_code == 403:
        authenticate()
        reserve_lunch(key,options_for_date,restur)
    repository.catch_options_to_repo(result)
    return result.status_code

def get_choosed_option(options,type):
    options = options[type]
    for index , key in enumerate(options):
        if options[key]==1:
            return key
    return "delete"


def get_lunch_response():
    result = request_for_card_pages()
    if result.status_code in [404, 403]:
        authenticate()
        get_lunch_response()
        return
    cache_csrf_for_user(result)
    return result


def request_for_card_pages():
    return requests.get(lunch_reserve_url, cookies=load_cookies("cookies"), headers=headers, allow_redirects=True)
