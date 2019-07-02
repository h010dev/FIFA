#!/bin/bash

for x in {1..10}; do (python3 -m scrapy crawl sofifa_redis_spider > ./$x.log ) & done
