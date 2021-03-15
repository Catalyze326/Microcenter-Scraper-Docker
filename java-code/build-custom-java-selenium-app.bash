#!/bin/bash
docker build -t java-app .
docker-compose down
docker-compose up -d
# Prints the output of the file for 30 seconds
timeout 30 docker logs -f "$(docker ps -aqf "name=java-app")"
