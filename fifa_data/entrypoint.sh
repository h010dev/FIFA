#!/bin/sh
apt-get update
apt-get install -y gcc

# LINE PROFILER

pip install Cython
git clone https://github.com/rkern/line_profiler.git
find line_profiler -name '*.pyx' -exec cython {} \;
cd line_profiler
pip install . --user
#apt install python3-line-profiler

# REDIS JSON

pip install rejson
git clone https://github.com/RedisJSON/RedisJSON.git
make

# OTHER PACKAGES

pip install -r /code/requirements.txt
/usr/local/bin/scrapyrt -i 0.0.0.0 -p 9080
