#!/bin/bash
cp main.py run-code/
pip freeze > run-code/requirements.txt
docker build -t microcenter-scraper-python ./run-code/
rm run-code/main.py
docker-compose up -d
timeout 30 docker logs -f "$(docker ps -aqf "name=microcenter-scraper-python")"

