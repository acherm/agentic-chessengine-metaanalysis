# Stockfish 18 — matches host binary + what corpus engines were originally
# measured against. We do NOT use UCI_LimitStrength/UCI_Elo as absolute
# anchor; SF's effective Elo at Skill Level {0,5,10,15} is empirically
# calibrated against external anchors (Rustic, Asymptote, Laser) in
# Phase A of the eval.
#
# Build:
#   docker build -t eval2/stockfish:18 docker/stockfish/

FROM debian:bookworm-slim AS build

ARG SF_TAG=sf_18
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential git ca-certificates wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
RUN git clone --depth 1 --branch ${SF_TAG} https://github.com/official-stockfish/Stockfish.git
WORKDIR /src/Stockfish/src
# Auto-detect target arch so the same Dockerfile builds natively on both
# x86_64 (CI) and arm64 (Apple Silicon dev). Stockfish 16.1 supports
# armv8 for arm64 and x86-64-modern for x86_64.
RUN ARCH=$(uname -m) && case "$ARCH" in \
      x86_64)        SF_ARCH=x86-64-modern ;; \
      aarch64|arm64) SF_ARCH=armv8 ;; \
      *) echo "Unsupported arch $ARCH" >&2; exit 1 ;; \
    esac && \
    make -j build ARCH="$SF_ARCH" && strip stockfish && cp stockfish /usr/local/bin/

FROM debian:bookworm-slim
COPY --from=build /usr/local/bin/stockfish /usr/local/bin/stockfish
LABEL eval2.role="reference" eval2.kind="stockfish" eval2.version="18"
ENTRYPOINT ["/usr/local/bin/stockfish"]
