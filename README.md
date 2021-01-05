# Microcenter Scraper Docker

The goal of this is to be able to deploy the microcenter scraper on you're server or local machine in a single command

Right now it uses a bash script that requires linux, but at some point I will make it compatable with Windows Subsystem for Linux (WSL)

On linux all you need to do in order to have a functioning system is to put your discord api key and other vals in as enviroment vars or just ignore that and use the nodejs frontend

You need to have docker and docker compose installed. I will have that linked here. https://docs.docker.com/get-docker/

## Setup you're own microcenter scraper (Visualization not finished)
```
bash runcode.bash
```

## How to use selenium remote with docker (Python and Java)

Python Dockerfile Must Include
```DOCKERFILE
EXPOSE 4444
```

Python with docker-compose
```PYTHON
from selenium import webdriver

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Remote(
    command_executor='http://selenium-appname:4444',
    options=firefox_options
)
```
Python with docker run
```PYTHON
from selenium import webdriver

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Remote(
    command_executor='http://localhost:4444',
    options=firefox_options
)
```
With docker run
```BASH
docker run -d -p 4444:4444 --name=selenium-appname -v /dev/shm:/dev/shm selenium/standalone-firefox:4.0.0-beta-1-prerelease-20201208
```
With Docker compose
```
services:
  selenium-appname:
    container_name: selenium-appname
    image:
      selenium/standalone-firefox:4.0.0-beta-1-prerelease-20201208
    ports:
    - 4444:4444
    volumes:
    - /dev/shm:/dev/shm
    networks:
      - network-name
  python-app:
    image:
      python-app
    container_name: python-app
    restart: unless-stopped
    networks:
      - network-name
networks:
  network-name:
    driver: bridge
```
For Docker-Compose Python Container (for bash script build must be in file named ./run-code/Dockerfile)
```DOCKERFILE
#RUN /opt/bin/generate_config > /opt/selenium/config.json
FROM python:3.8
# set the working directory in the container
COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt
# copy the content of the local src directory to the working directory
COPY main.py .
# command to run on container start
CMD [ "python", "./main.py" ]

EXPOSE 4444
```
For Docker-Compose build docker container and run docker-compose (Python)
```BASH
build-custom-python-selenium-app.bash
```
Contents of that file (Python)
```BASH
#!/bin/bash
mkdir run-code/
cp main.py run-code/
pip freeze > run-code/requirements.txt
docker build -t python-app ./run-code/
rm run-code/main.py
docker-compose down
docker-compose up -d
timeout 30 docker logs -f "$(docker ps -aqf "name=python-app")"
```
This needs to rebuild the app in gradle every time and does not cache the dependencies, so it takes a while to build every time you change the code that is on my todo list

For Docker-Compose Java Container (Only works with gradle for now) (for bash script build must be in file named ./Dockerfile) (replace rootProject.name with the value in settings.gradle of rootProject.name)

Java Code with docker-compose
```JAVA
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.WebDriver;
import java.net.URL;

FirefoxOptions options = new FirefoxOptions();
Url url = new URL("http://selenium-appname:4444")
WebDriver driver = new RemoteWebDriver(url , options);
```
Java Code with docker run
```JAVA
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.WebDriver;
import java.net.URL;

FirefoxOptions options = new FirefoxOptions();
Url url = new URL("http://localhost:4444")
WebDriver driver = new RemoteWebDriver(url , options);
```
Dockerfile must be put in ./Dockerfile
```DOCKERFILE
FROM gradle:5.3.0-jdk-alpine AS TEMP_BUILD_IMAGE
ENV APP_HOME=/usr/app/
WORKDIR $APP_HOME
COPY build.gradle settings.gradle $APP_HOME

COPY gradle $APP_HOME/gradle
COPY --chown=gradle:gradle . /home/gradle/src
USER root
RUN chown -R gradle /home/gradle/src
    
RUN gradle fatJar || return 0
COPY . .
RUN gradle clean fatJar
    
# actual container
FROM adoptopenjdk/openjdk11:alpine-jre
ENV ARTIFACT_NAME=rootProject.name-1.0-SNAPSHOT.jar
ENV APP_HOME=/usr/app/
    
WORKDIR $APP_HOME
COPY --from=TEMP_BUILD_IMAGE $APP_HOME/build/libs/$ARTIFACT_NAME .

ENTRYPOINT exec java -jar ${ARTIFACT_NAME}

EXPOSE 4444
```
build.gradle must create a fatJar (Replace PACKAGENAME.MAINCLASS with you're packagename.mainclass)
```GRADLE
plugins {
    id 'java'
}

group 'org.example'
version '1.0-SNAPSHOT'

repositories {
    mavenCentral()
}

dependencies {
    compile group: 'org.seleniumhq.selenium', name: 'selenium-java', version: '3.141.59'
}

task fatJar(type: Jar) {
    manifest {
        attributes 'Main-Class': 'PACKAGE_NAME.MAINCLASS'
    }
    from { configurations.compile.collect { it.isDirectory() ? it : zipTree(it) } }
    with jar
}
```

With docker run
```BASH
docker run -d -p 4444:4444 --name=selenium-appname -v /dev/shm:/dev/shm selenium/standalone-firefox:4.0.0-beta-1-prerelease-20201208
```
With Docker compose
```
services:
  selenium-appname:
    container_name: selenium-appname
    image:
      selenium/standalone-firefox:4.0.0-beta-1-prerelease-20201208
    ports:
    - 4444:4444
    volumes:
    - /dev/shm:/dev/shm
    networks:
      - network-name
  java-app:
    image:
      java-app
    container_name: java-app
    restart: unless-stopped
    networks:
      - network-name
networks:
  network-name:
    driver: bridge
```
For Docker-Compose build docker container and run docker-compose (Python)
```BASH
build-custom-java-selenium-app.bash
```
Contents of that file (Java)
```BASH
#!/bin/bash
docker build -t java-app .
docker-compose down
docker-compose up -d
# Prints the output of the file for 30 seconds
timeout 30 docker logs -f "$(docker ps -aqf "name=java-app")"
```