#!/bin/bash

source ./fifa_data/file.txt

declare -i urls=$url_count

usage()
{
	echo "usage: 
-s split        Number of url splits to perform - this will determine the total
                number of spiders to be run. 
		
		Example: url_count = 10000, split = 1000
		Number of spiders = url_count / split = 10
-h help"
}

while [ "$1" != "" ]; do
	case $1 in
		-s | --split )		shift
					declare -i split=$1
					;;
		-h | --help )		usage
					exit
					;;
		* )			usage
					exit 1
	esac
	shift

	if [ $urls -ne 0 ]; then

		spiders=$(( $urls / $split + 1 ))

		for i in $(seq 1 $spiders); do
			curl http://localhost:6800/schedule.json \
				-d project=fifa_data \
				-d spider=sofifa_redis_club_pages
		done
	else
		echo "URL list is empty!"
	fi
done
