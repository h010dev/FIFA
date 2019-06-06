#!/bin/bash

echo "Starting up docker-compose ... "

newgrp docker

docker-compose -f docker-compose-LocalExecutor.yml up -d
