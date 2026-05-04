# chess-assembly-codex — Tier A. x86/ARM assembly CORE + Python UCI bridge.
# Repo's Makefile is macOS-only (clang -dynamiclib → .dylib). We rewrite
# the core build step for Linux (clang -shared → .so) and keep the
# Python UCI bridge unchanged.
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential clang \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
# The Makefile builds src/core/core.s → build/libasm_core.dylib via:
#   clang -arch arm64 -O3 -dynamiclib src/core/core.s -o build/libasm_core.dylib
# For Linux we produce a .so instead. Pick arch from the build platform.
RUN mkdir -p build && \
    ARCH=$(uname -m) && case "$ARCH" in \
      x86_64)        ARCH_FLAG="" ;; \
      aarch64|arm64) ARCH_FLAG="" ;; \
      *) echo "unsupported arch $ARCH"; exit 1 ;; \
    esac && \
    clang -O3 -fPIC -shared src/core/core.s src/core/core_impl.c \
      -o build/libasm_core.so $ARCH_FLAG

FROM python:3.11-slim
COPY --from=build /opt/engine/build /opt/engine/build
COPY --from=build /opt/engine/scripts /opt/engine/scripts
COPY --from=build /opt/engine/src /opt/engine/src
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-assembly-codex" eval2.tier="A"
ENTRYPOINT ["python3", "-u", "scripts/uci_bridge.py", "--core", "build/libasm_core.so", "--depth", "6"]
