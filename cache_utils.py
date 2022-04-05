import redis, json
import hashlib
from utilities import *
from bs4_utils import *
conn = redis.Redis('localhost',decode_responses=True)
ex = 200


def write_dic_to_cache(cache_name, dic):
    conn.set(cache_name, json.dumps(dic), ex=ex)


def get_dic_from_cache(cache_name):
    return json.loads(conn.get(cache_name))


def write_key_to_cache(key, value):
    conn.set(key, value, ex=ex)


def get_key_from_cache(key):
    return conn.get(key)



# def get_choice_hash(response):
#     soup = convert_to_soup(response)
#     reservation = soup.find_all("p", {"id": "text"})
#     choice_hash = hashlib.md5(str(reservation).encode("utf-8")).digest()
#     write_key_to_cache("choice_hash", choice_hash)
#     return choice_hash

def cache_choices(choices):
    choice_hash = hashlib.md5(str(choices).encode("utf-8")).digest()
    write_key_to_cache("choice_hash", choice_hash)
    return choice_hash

def choices_from_cache():
    pass


def update_cache_if_needed(result):
    pass

def cache_csrf_for_user(soup):
    token = get_new_csrf(soup)
    write_key_to_cache("csrf",token)

def get_cached_csrf_token_for_user():
    return get_key_from_cache("csrf")