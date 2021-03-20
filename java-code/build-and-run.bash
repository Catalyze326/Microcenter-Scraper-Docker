#!/bin/bash
docker build -t microcenter-java .
docker-compose down
docker-compose up -d
docker logs -f "$(docker ps -aqf "name=microcenter-java")"