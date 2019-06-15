import pymongo
import json
from pprint import pprint
from pymongo import MongoClient
from fifa_data.mongodb_addr import host


def get_proxies(filename):

    """
    Retrieve proxies from json storage. This is used as an initialization
    file to be used by the proxy rotator before the spiders collect fresh
    proxies.
    """

    input_file = open(filename)
    json_array = json.load(input_file)

    return json_array


def initdb():

    """
    This will dump the stored proxies into the proxy database. Running
    this assumes that the database is empty. Otherwise run updatedb instead.
    """

    init_operations = [pymongo.operations.InsertOne(
        {"ip": ip["ip"]}
    ) for ip in new_proxies]

    result = collection.bulk_write(init_operations)

    try:
        return result
    finally:
        pprint(result.bulk_api_result)


def updatedb():

    """
    This will update the proxy database with new ones from storage. This
    is to be used when the proxy database has a few entries, as it will
    skip duplicates.
    """

    operations = [pymongo.operations.UpdateOne(
        filter={"ip": ip["ip"]},
        update={"$setOnInsert": {"ip": ip["ip"]}},
        upsert=True
        ) for ip in new_proxies]

    result = collection.bulk_write(operations)

    try:
        return result
    finally:
        pprint(result.bulk_api_result)


if __name__ == '__main__':

    import os

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'proxy_storage.json')

    client = MongoClient(host, 27017)
    db = client.agents_proxies
    collection = db.proxies

    new_proxies = get_proxies(filename=filename)

    if db.proxies.count_documents(filter=({})) < 1:
        initdb()
    else:
        updatedb()
