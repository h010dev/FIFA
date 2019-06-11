#!/bin/bash

mongo --quiet agents_proxies --eval \
	'printjson(
                db.proxies.find({},
		{
			"_id": 0,
			"ip": 1
		}).toArray())' \
			> /home/camillitea/FIFA/fifa_data/proxies/proxy_storage.json
