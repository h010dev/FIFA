import random
from datetime import datetime, timedelta

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

    query = collection.find(
        {"$and": [
            {'time_stamp': {'$gte': datetime.utcnow() - timedelta(days=1)},
             'type': 'https',
             'response_time': {'$lte': 2.5}}
        ]},
        {'_id': 0, 'ip': 1}
    )

    proxies = [x['ip'] for x in query]
    random.shuffle(proxies)

    print(proxies)
    print(len(proxies))
    return proxies


if __name__ == '__main__':
    gen_proxy_list()
