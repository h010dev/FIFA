#!/bin/bash

mongo --quiet agents_proxies --eval \
	'printjson(
		db.user_agents.find({
			"$and": [
				{"$or": [
						{"OS": "Windows"}, 
						{"OS": "Mac OS X"}, 
						{"OS": "macOS"}, 
						{"OS": "Linux"}
					]
				}, 
				{"$or": [
						{"hardware_type": "Computer"}, 
						{"hardware_type": "Windows"}, 
						{"hardware_type": "Linux"}, 
						{"hardware_type": "Mac"}
					]
				}, 
				{"$or": [
						{"popularity": "Very common"}, 
						{"popularity": "Common"}
					]
				}
				]},
			{
				"_id": 0, 
				"user_agent": 1, 
				"version": 1, 
				"OS": 1, 
				"hardware_type": 1, 
				"popularity": 1
			}).toArray())' \
			> ./useragent_storage.json
