FROM gradle:5.3.0-jdk-alpine AS TEMP_BUILD_IMAGE
ENV APP_HOME=/usr/app/
WORKDIR \$APP_HOME
COPY build.gradle settings.gradle \$APP_HOME/

COPY gradle \$APP_HOME/gradle
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

WORKDIR \$APP_HOME
COPY --from=TEMP_BUILD_IMAGE \$APP_HOME/build/libs/\$ARTIFACT_NAME .

ENTRYPOINT exec java -jar \${ARTIFACT_NAME}

EXPOSE 4444