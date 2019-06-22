import json
from pprint import pprint
import pymongo
from pymongo import MongoClient
from fifa_data.mongodb_addr import host


def get_useragents(filename):

    """
    Retrieve user-agents from json storage. This is used as an
    initialization file to be used by the user-agent rotator before the
    spiders collect fresh user-agents.
    """

    input_file = open(filename)
    json_array = json.load(input_file)

    return json_array


def updatedb():

    """
    This will update the user-agent database with new ones from
    storage. This is to be used when the user-agent database has a few
    entries, as it will skip duplicates.
    """

    operations = [pymongo.operations.UpdateOne(
        {"$and": [
            {"user_agent": agent["user_agent"],
             "version": agent["version"],
             "OS": agent["OS"],
             "hardware_type": agent["hardware_type"],
             "popularity": agent["popularity"]}
        ]},
        {
            "$setOnInsert":
                {"user_agent": agent["user_agent"]},
        },
        upsert=True
    ) for agent in new_useragents if "version" in agent]

    result = collection.bulk_write(operations)

    try:
        return result
    finally:
        pprint(result.bulk_api_result)


if __name__ == '__main__':

    import os

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'useragent_storage.json')

    client = MongoClient(host, 27017)
    db = client.agents_proxies
    collection = db.user_agents

    new_useragents = get_useragents(filename=filename)

    updatedb()
