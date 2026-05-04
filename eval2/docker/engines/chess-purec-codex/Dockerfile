# chess-purec-codex — Tier A. Makefile produces build/purec_chess.
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN make && strip build/purec_chess

FROM debian:bookworm-slim
COPY --from=build /opt/engine/build/purec_chess /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-purec-codex" eval2.tier="A"
ENTRYPOINT ["/usr/local/bin/engine"]
