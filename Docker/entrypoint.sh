#!/bin/sh

apt-get update
pip install -r /code/requirements.txt
/usr/local/bin/scrapyrt -i 0.0.0.0 -p 9080
