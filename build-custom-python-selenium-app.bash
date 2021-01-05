#!/bin/bash
mkdir run-code/
cp main.py run-code/
pip freeze > run-code/requirements.txt
docker build -t python-app ./run-code/
rm run-code/main.py
docker-compose down
docker-compose up -d
timeout 30 docker logs -f "$(docker ps -aqf "name=python-app")"