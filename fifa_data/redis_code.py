from datetime import datetime
from pprint import pprint
from rejson import Client, Path


rj = Client(host='localhost', port=6379, decode_responses=True)

# Get single key:value pair
pprint(rj.jsonget("redis_club_urls:item73", Path.rootPath()))

# Convert timestamp from iso to datetime
timestamp = rj.jsonget("redis_club_urls:item73", Path.rootPath())['last_modified']
timestamp = datetime.fromisoformat(timestamp)

# Get all keys
print(rj.keys())

# Get all values matching pattern from keys
for key in rj.scan_iter("redis_club_urls:item:*"):
    print(rj.jsonget(key, Path('.club_page')))

# Add all values matching pattern to new key
for key in rj.scan_iter("redis_club_urls:item:*"):
    val = rj.jsonget(key, Path('.club_page'))
    rj.sadd('all_urls', val)
