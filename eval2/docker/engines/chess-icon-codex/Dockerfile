# chess-icon-codex — Tier B. Icon language (icont compiler).
# Icon is not packaged in Debian; we build it from source. This image
# is heavier than the others as a result.
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libx11-dev wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /tmp
RUN wget -q https://www2.cs.arizona.edu/icon/ftp/packages/unix/icon-v951src.tgz \
 && tar -xzf icon-v951src.tgz \
 && cd icon-v951src && make X-Configure name=linux && make Samples
ENV PATH=/tmp/icon-v951src/bin:$PATH

COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN icont engine.icn

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libx11-6 && rm -rf /var/lib/apt/lists/*
COPY --from=build /tmp/icon-v951src/bin/iconx /usr/local/bin/iconx
COPY --from=build /opt/engine/engine /opt/engine/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-icon-codex" eval2.tier="B"
ENTRYPOINT ["./engine"]
