import redis, json
conn = redis.Redis('localhost')
ex = 10


def write_dic_to_cache(cache_name, dic):
    conn.set(cache_name, json.dumps(dic), ex=ex)


def get_dic_from_cache(cache_name):
    return json.loads(conn.get(cache_name))


def write_key_to_cache(key, value):
    conn.set(key, value, ex=ex)


def get_key_from_cache(key):
    return conn.get(key)