# chess-purec — Tier A, C bitboard engine. Binary is `purec`.
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
# `make` produces a binary whose name depends on the Makefile's TARGET
# variable; on the host the artifact is called `purec`.
# Clean any pre-built artefacts the host repo may carry (Mac binaries
# leak through rsync) before rebuilding fresh inside the container.
RUN rm -f purec chess engine && make && strip purec

FROM debian:bookworm-slim
COPY --from=build /opt/engine/purec /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-purec" eval2.tier="A"
ENTRYPOINT ["/usr/local/bin/engine"]
