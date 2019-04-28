from pymongo import MongoClient
import random


client = MongoClient('localhost', 27017)
db = client.sofifa
collection = db.proxies

proxies = [x['ip'] for x in collection.find()]

random.shuffle(proxies)
