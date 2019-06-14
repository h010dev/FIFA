#!/bin/bash

mongo --quiet agents_proxies --eval \
	'printjson(
                db.proxies.find({},
		{
			"_id": 0,
			"ip": 1
		}).toArray())' \
			> ./proxy_storage.json
