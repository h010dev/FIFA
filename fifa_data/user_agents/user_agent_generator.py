from pymongo import MongoClient
import random


client = MongoClient('mongo', 27017)
db = client.agents_proxies
collection = db.user_agents

query = collection.find({
    '$and': [
        {'$or': [
            {'OS': 'Windows'},
            {'OS': 'Mac OS X'},
            {'OS': 'macOS'},
            {'OS': 'Linux'}
        ]},
        {'$or': [
            {'hardware_type': 'Computer'},
            {'hardware_type': 'Windows'},
            {'hardware_type': 'Linux'},
            {'hardware_type': 'Mac'}
        ]},
        {'$or': [
            {'popularity': 'Very common'},
            {'popularity': 'Common'}
        ]}
    ]
    },
        {'_id': 0, 'user_agent': 1}
)

user_agent = [x['user_agent'] for x in query]

random.shuffle(user_agent)
