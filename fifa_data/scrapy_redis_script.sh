#!/bin/bash

for x in {1..10}; do (python3 -m scrapy crawl sofifa_club_pages > ./$x.log ) & done
