#!/bin/bash
cp main.py run-code/
pip freeze > run-code/requirements.txt
docker build -t microcenter-scraper-python ./run-code/
rm run-code/main.py
cp main.py discord-bot/
pip freeze > discord-bot/requirements.txt
docker build -t microcenter-discord-bot ./discord-bot/
rm microcenter-discord-bot/discord.py
docker-compose down
docker-compose up -d
timeout 30 docker logs -f "$(docker ps -aqf "name=microcenter-scraper-python")"

