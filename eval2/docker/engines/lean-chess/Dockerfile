# lean-chess — Tier B. Lean 4 with lake; toolchain pinned by lean-toolchain
# inside the source. The default executable target is `leanchess`.
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
ENV ELAN_HOME=/opt/elan
ENV PATH=/opt/elan/bin:/root/.elan/bin:$PATH
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf \
    | sh -s -- -y --default-toolchain none
COPY src/ /opt/engine/
WORKDIR /opt/engine
# elan auto-installs the toolchain referenced by lean-toolchain on first use.
RUN lake build leanchess

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libgmp10 && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/engine/.lake/build/bin/leanchess /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="lean-chess" eval2.tier="B"
ENTRYPOINT ["/usr/local/bin/engine"]
