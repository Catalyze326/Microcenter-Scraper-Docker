FROM gradle:jdk11-hotspot as cache
RUN mkdir -p /home/gradle/cache_home
ENV GRADLE_USER_HOME /home/gradle/cache_home
COPY build.gradle /home/gradle/java-code/
WORKDIR /home/gradle/java-code
RUN gradle clean build -i --stacktrace

FROM gradle:jdk11-hotspot AS TEMP_BUILD_IMAGE
COPY --from=cache /home/gradle/cache_home /home/gradle/.gradle
COPY --chown=gradle:gradle . /home/gradle/src
WORKDIR /home/gradle/src
RUN gradle jar --no-daemon || return 0

# actual container
FROM adoptopenjdk/openjdk11:alpine-jre
WORKDIR \$APP_HOME
ENV ARTIFACT_NAME=java-kotlin-microcenter-1.0-SNAPSHOT.jar
COPY --from=TEMP_BUILD_IMAGE /home/gradle/src/build/libs/*.jar .
ENTRYPOINT exec java -jar ${ARTIFACT_NAME}
EXPOSE 4444