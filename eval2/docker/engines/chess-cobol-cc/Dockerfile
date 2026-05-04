# chess-cobol-cc — Tier B. Source is chess-engine.cob; the host repo
# also ships pre-built Mach-O binaries which won't run in Linux. We
# rebuild from source via gnucobol.
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gnucobol4 \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN cobc -O3 -x chess-engine.cob -o chess-engine

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      libcob4 libcob5 libgmp10 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/engine/chess-engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-cobol-cc" eval2.tier="B"
ENTRYPOINT ["/usr/local/bin/engine"]
