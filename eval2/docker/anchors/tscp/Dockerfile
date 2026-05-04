# TSCP 1.81 — Tom Kerrigan's Simple Chess Program. Public domain.
# CCRL 40/4 ≈ 1750 Elo. Used as a low-mid anchor.
#
# TSCP is not natively UCI; it speaks an old custom protocol. We wrap it
# with a tiny xboard→UCI adapter (polyglot from CuteChess project, packaged
# here as `polyglot`) so cutechess-cli can drive it as UCI.
#
# Build:
#   docker build -t eval2/anchor-tscp181 docker/anchors/tscp/

FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential wget unzip ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
# Source is hosted at tckerrigan.com/Chess/TSCP/. The 1.81 distribution
# ships only .c/.h files (no Makefile), so we compile directly with gcc.
ADD https://www.tckerrigan.com/Chess/TSCP/tscp181.zip tscp181.zip
RUN unzip tscp181.zip \
    && cd tscp181 \
    && gcc -O2 -o tscp main.c board.c book.c data.c eval.c search.c

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      polyglot \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /src/tscp181/tscp /usr/local/bin/tscp
COPY tscp.cfg /etc/tscp/polyglot.cfg
LABEL eval2.role="anchor" eval2.kind="external" eval2.engine="tscp" eval2.version="1.81" eval2.ccrl_40_4="1750"
# Debian installs polyglot at /usr/games/polyglot, which is outside the
# default non-interactive PATH; use absolute path.
ENTRYPOINT ["/usr/games/polyglot", "/etc/tscp/polyglot.cfg"]
