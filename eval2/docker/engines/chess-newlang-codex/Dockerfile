# chess-newlang-codex — Tier A (DSL design + C++ transpile).
# The GAMBIT DSL compiles .gmb files to C++17. Build process:
#   pip install -e .            # install `gambit` CLI
#   gambit build . -o ./engine  # transpile + compile
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential g++ python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN python3 -m pip install --break-system-packages -e . \
 && gambit build . -o ./engine \
 && test -x engine

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libstdc++6 && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/engine/engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-newlang-codex" eval2.tier="A" \
      eval2.flag="dsl-special-role"
ENTRYPOINT ["/usr/local/bin/engine"]
