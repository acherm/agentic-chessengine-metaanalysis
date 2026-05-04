# cplusplus-chess — Tier A, C++ with CMake. Executable is `cplusplus_chess`.
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
 && cmake --build build -j --target cplusplus_chess \
 && strip build/cplusplus_chess

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libstdc++6 && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/engine/build/cplusplus_chess /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="cplusplus-chess" eval2.tier="A"
ENTRYPOINT ["/usr/local/bin/engine"]
