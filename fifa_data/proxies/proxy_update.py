import pymongo
from pymongo import MongoClient
import json
from pprint import pprint


client = MongoClient('mongo', 27017)
db = client.agents_proxies
collection = db.fate0_proxy_list

FILE_NAME = r"C:\Users\E46Racing\Documents\PycharmProjects\my_projects\fifa_workspace\fifa_market_analysis" \
            r"\fate0_proxy_list.json"


def get_proxies(filename):

    input_file = open(filename)
    json_array = json.load(input_file)

    return json_array


new_proxies = get_proxies(filename=FILE_NAME)

# INITIAL IMPORT

# init_operations = [pymongo.operations.InsertOne(
#     {"country": ip["country"],
#      "port": ip["port"],
#      "type": ip["type"],
#      "response_time": ip["response_time"],
#      "host": ip["host"],
#      "from": ip["from"],
#      "anonymity": ip["anonymity"],
#      "export_address": ip["export_address"]}
# ) for ip in new_proxies]
#
# init_result = db.collection.bulk_write(init_operations)
#
# init_result
#
# pprint(init_result.bulk_api_result)

# SUBSEQUENT UPDATES

operations = [pymongo.operations.UpdateOne(
    filter={"host": ip["host"]},
    # replacement=ip,
    update={"$setOnInsert": {"host": ip["host"]}},
    upsert=True
    ) for ip in new_proxies]

result = db.collection.bulk_write(operations)

result
pprint(result.bulk_api_result)

# for ip in new_proxies:
#     if not collection.find_one({"host": ip["host"]}):
#         pymongo.operations.InsertOne(
#             {"country": ip["country"],
#              "port": ip["port"],
#              "type": ip["type"],
#              "response_time": ip["response_time"],
#              "host": ip["host"],
#              "from": ip["from"],
#              "anonymity": ip["anonymity"],
#              "export_address": ip["export_address"]}
#         )
#     else:
#         continue
