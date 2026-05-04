# chess-java — Tier B, Codex JVM engine.
# Repo's pom.xml is incomplete (no Main-Class); the agent built this
# with scripts/build.sh (plain javac --release 11). Main class is
# com.example.chess.UciMain, classes compiled to build/classes/.
FROM eclipse-temurin:21-jdk AS build
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN scripts/build.sh

FROM eclipse-temurin:21-jre
COPY --from=build /opt/engine/build/classes /opt/engine/build/classes
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-java" eval2.tier="B"
ENTRYPOINT ["java", "-Xss2m", "-Xmx384m", "-cp", "/opt/engine/build/classes", "com.example.chess.UciMain"]
