import init
import request_utils
from cache_utils import get_dic_from_cache
def fetch_options_from_repo():
    try:
        return get_dic_from_cache("options_index")
    except TypeError as e:
        result = request_utils.get_lunch_response()
        return init.index_options(result)
def catch_options_to_repo(result):
    return init.index_options(result)
