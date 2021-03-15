FROM gradle:jdk11-hotspot AS TEMP_BUILD_IMAGE

COPY --chown=gradle:gradle . /home/gradle/src
WORKDIR /home/gradle/src
RUN gradle jar --no-daemon || return 0

# actual container
#FROM adoptopenjdk/openjdk11:alpine-jre
#ENV ARTIFACT_NAME=Microcenter-Scraper-Docker-Java-1.0-SNAPSHOT.jar
#ENV APP_HOME=/home/gradle/src

#WORKDIR \$APP_HOME
#ENV ARTIFACT_NAME=java-kotlin-microcenter-1.0-SNAPSHOT.jar
#COPY --from=TEMP_BUILD_IMAGE /home/gradle/src/build/libs/*.jar .
#
#ENTRYPOINT exec java -jar \${ARTIFACT_NAME}
#
#EXPOSE 4444

FROM adoptopenjdk/openjdk11:alpine-jre
ENV ARTIFACT_NAME=java-kotlin-microcenter-1.0-SNAPSHOT.jar
ENV APP_HOME=/usr/app/

WORKDIR \$APP_HOME
COPY --from=TEMP_BUILD_IMAGE \$APP_HOME/build/libs/\$ARTIFACT_NAME .

ENTRYPOINT exec java -jar \${ARTIFACT_NAME}

EXPOSE 4444