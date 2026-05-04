# chess-java-cc — Tier B, JVM engine. Maven, not Gradle.
FROM maven:3.9-eclipse-temurin-21 AS build
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN mvn -B -ntp -DskipTests package

FROM eclipse-temurin:21-jre
COPY --from=build /opt/engine/target /opt/engine/target
WORKDIR /opt/engine
RUN sh -c 'jar=$(ls target/*.jar | grep -v sources | grep -v javadoc | head -1) && cp "$jar" /opt/engine/engine.jar'
LABEL eval2.role="engine" eval2.engine="chess-java-cc" eval2.tier="B"
ENTRYPOINT ["java", "-Xss2m", "-Xmx384m", "-jar", "/opt/engine/engine.jar"]
