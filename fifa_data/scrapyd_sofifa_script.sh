#!/bin/bash

for ((i = 1 ; i < 11 ; i ++)); do
	curl http://localhost:6800/schedule.json -d project=fifa_data -d spider=club_details_spider_$i
done
