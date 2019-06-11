import pymongo
from pymongo import MongoClient
from fifa_data.mongodb_addr import host
import json
from pprint import pprint


client = MongoClient(f'{host}', 27017)
db = client.agents_proxies
collection = db.user_agents

FILE_NAME = '/FIFA/fifa_data/user_agents/useragent_storage.json'


def get_useragents(filename):

    input_file = open(filename)
    json_array = json.load(input_file)

    return json_array


new_useragents = get_useragents(filename=FILE_NAME)

# INITIAL IMPORT

def initdb():

    init_operations = [pymongo.operations.InsertOne(
        {"user_agent": agent["user_agent"],
         "version": agent["version"],
         "OS": agent["OS"],
         "hardware_type": agent["hardware_type"],
         "popularity": agent["popularity"]}
    ) for agent in new_useragents if "version" in agent]

    init_result = collection.bulk_write(init_operations)

    init_result

    pprint(init_result.bulk_api_result)

# SUBSEQUENT UPDATES

def updatedb():

    operations = [pymongo.operations.UpdateOne(
        filter={"user_agent": agent["user_agent"]},
        update={"$setOnInsert": {"user_agent": agent["user_agent"]}},
        upsert=True
        ) for agent in new_useragents]

    result = collection.bulk_write(operations)

    result
    pprint(result.bulk_api_result)


if __name__=='__main__':
    if db.user_agents.find({}).count() < 1:
        initdb()
    else:
        updatedb()
