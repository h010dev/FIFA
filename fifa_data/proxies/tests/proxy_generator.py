import atexit
import cProfile
import line_profiler
import pstats
import random
from datetime import datetime, timedelta
from pstats import SortKey

from pymongo import MongoClient
from fifa_data.mongodb_addr import host, port

profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)


@profile
def gen_proxy_list():

    """
    Generate a list of proxies from the proxy database. This list will
    be used by the proxy rotator.
    """

    client = MongoClient(host, port)
    db = client.agents_proxies
    collection = db.proxies

    query = collection.find({
        'last_modified': {'$gte': datetime.utcnow() - timedelta(days=1)}
    },
        {'_id': 0, 'ip': 1}
    )

    proxies = [x['ip'] for x in query]
    random.shuffle(proxies)

    return proxies


if __name__ == '__main__':
#    cProfile.run('gen_proxy_list()', 'restats')
#    p = pstats.Stats('restats')
#    p.strip_dirs().sort_stats(SortKey.CUMULATIVE).dump_stats('mystats.txt')
    gen_proxy_list()
