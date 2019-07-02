#!/bin/bash

for x in {1..10}; do (curl http://localhost:6800/schedule.json -d project=fifa_data -d spider=sofifa_redis_spider) & done
