# CPW-Engine — the Chess Programming Wiki tutorial engine.
# CCRL 40/4 ≈ 1470–1500 (version 1.1). Used as the low anchor.
# Source: https://github.com/nescitus/cpw-engine
#
# Native UCI, plain C++, trivial build.

FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/nescitus/cpw-engine.git
WORKDIR /src/cpw-engine
# Repo ships a Makefile; fall back to direct g++ call if that fails.
RUN (make) \
 || (g++ -O3 -std=c++17 -o cpw-engine *.cpp) \
 || (g++ -O3 -std=c++11 -o cpw-engine *.cpp) \
 || (echo "cpw-engine build failed; inspect repo layout" >&2; exit 1)
RUN strip cpw-engine 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /src/cpw-engine/cpw-engine /usr/local/bin/cpw-engine
LABEL eval2.role="anchor" eval2.kind="external" eval2.engine="cpw-engine" eval2.ccrl_40_4="1470"
ENTRYPOINT ["/usr/local/bin/cpw-engine"]
