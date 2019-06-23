from datetime import datetime
from pprint import pprint

import pymongo
from pymongo import MongoClient


def updatedb():

    operations = [pymongo.operations.UpdateOne(
        {"$and": [
            {"anonymity": d["anonymity"],
             "export_address": d["export_address"],
             "response_time": d["response_time"],
             "port": d["port"],
             "country": d["country"],
             "host": d["host"],
             "type": d["type"],
             "from": d["from"],
             "time_stamp": datetime.utcnow()}
        ]},
        {"$setOnInsert": {"ip": str(
            str(d["type"])
            + '://'
            + str(d["host"])
            + ':'
            + str(d["port"])
        )}},
        upsert=True
    ) for d in pd]

    result = collection.bulk_write(operations)

    try:
        return result
    finally:
        pprint(result.bulk_api_result)


if __name__ == '__main__':

    proxy_file = open('proxy_list.txt', 'r')
    proxy_list = proxy_file.readlines()

    client = MongoClient('localhost', 27017)
    db = client.agents_proxies
    collection = db.proxy_test

    pd = list()
    null = None

    for i in range(len(proxy_list)):
        pd.append(eval(proxy_list[i]))

    updatedb()
