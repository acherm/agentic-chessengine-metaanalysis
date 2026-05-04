# chess-cplusplus-claude — Tier A, "Claudius" engine.
# CMakeLists declares add_executable(engine ...) plus a perft_test target.
# Build only the `engine` target so a perft_test compile failure doesn't
# kill the engine image.
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential cmake \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
# GCC 12 requires explicit <cstring> for std::memset; the engine's
# headers omit it (relied on Apple clang's transitive include). Inject
# it globally via CXXFLAGS rather than patching upstream sources.
RUN CXXFLAGS="-include cstring" cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
 && cmake --build build -j --target engine \
 && strip build/engine

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libstdc++6 && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/engine/build/engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-cplusplus-claude" eval2.tier="A"
ENTRYPOINT ["/usr/local/bin/engine"]
