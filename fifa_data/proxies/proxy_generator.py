import random
from pymongo import MongoClient
from fifa_data.mongodb_addr import host, port


def gen_proxy_list():

    """
    Generate a list of proxies from the proxy database. This list will
    be used by the proxy rotator.
    """

    client = MongoClient(host, port)
    db = client.agents_proxies
    collection = db.proxies

    proxies = [x['ip'] for x in collection.find({'ip': {"$exists": True}})]
    random.shuffle(proxies)

    return proxies


if __name__ == '__main__':
    gen_proxy_list()
