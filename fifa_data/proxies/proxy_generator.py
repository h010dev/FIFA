from pymongo import MongoClient
from fifa_data.mongodb_addr import host
import random


def gen_proxy_list():

    client = MongoClient(f'{host}', 27017)
    db = client.sofifa
    collection = db.proxies

    proxies = [x['ip'] for x in collection.find()]

    random.shuffle(proxies)

    print(proxies)

    return proxies


if __name__=='__main__':
    gen_proxy_list()
