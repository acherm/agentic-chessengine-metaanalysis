# COBOL-chess — Tier B. GNU COBOL.
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gnucobol4 \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
# Wipe any pre-built host (Mach-O) binaries that leak through rsync;
# the Makefile's `bin/cobochess` target rebuilds from source.
RUN rm -rf bin && mkdir bin && make bin/cobochess

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      libcob4 libcob5 libgmp10 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/engine/bin/cobochess /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="COBOL-chess" eval2.tier="B"
ENTRYPOINT ["/usr/local/bin/engine"]
