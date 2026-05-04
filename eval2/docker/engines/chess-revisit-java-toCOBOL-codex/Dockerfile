# chess-revisit-java-toCOBOL-codex — Java→COBOL port (special-role).
# Source at src/cobol/chess_engine.cob. Build with `cobc -x -free`.
# Uses gnucobol 5 (Debian trixie). The port's COBOL source uses B-XOR
# which is gnucobol 5+ only; bookworm's gnucobol4 is too old.
FROM debian:trixie-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gnucobol \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN cobc -x -free -O3 src/cobol/chess_engine.cob -o chess_engine

FROM debian:trixie-slim
# Trixie uses t64-suffixed libcob names. The compiled binary may link to
# either libcob.so.4 or .so.5 depending on how gnucobol was packaged;
# install both for safety.
RUN apt-get update && apt-get install -y --no-install-recommends \
      libcob4t64 libcob5t64 libgmp10 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/engine/chess_engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-revisit-java-tocobol-codex" eval2.tier="B" \
      eval2.flag="port-special-role"
ENTRYPOINT ["/usr/local/bin/engine"]
