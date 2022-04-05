from cache_utils import *
from redis import Redis
from rq import Queue

from test2 import *
# import datetime
# user = {"Name": "Pradeep", "Company": {"dd":"dddd"}, "Address": "Mumbai", "Location": "RCP"}
# #write_dic_to_cache("abbass",user)
# date1 = datetime.datetime.now()
# date2 = date1.replace(hour=23, minute=59, second=59)
# print(datetime.datetime.now())
# try:
#     a = get_dic_from_cache("abbass")
# except TypeError as e:
#     print(e)

# a = {}
# a["asb"] = {}
# a["asb"]["assari"] = 2
# a["asb"]["asssdfsari"] =3
#
# print(a)



q = Queue(connection=Redis())

for i in range(10):
    print(q.enqueue(do_some))