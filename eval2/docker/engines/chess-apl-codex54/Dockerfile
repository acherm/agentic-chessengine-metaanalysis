# chess-apl-codex54 — Tier B. Uses GNU APL (free), NOT Dyalog — per session logs.
# GNU APL is NOT packaged in Debian bookworm/trixie or Ubuntu 22.04 repos,
# so we build it from source. Slow first build (~3 min); cached after.
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential wget ca-certificates libreadline-dev libncurses-dev \
      libpcre3-dev libsqlite3-dev \
      autoconf automake autoconf-archive \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /tmp
# GNU APL upstream. Tag apl-1.8 is the latest widely-compiled release.
RUN wget -q https://ftp.gnu.org/gnu/apl/apl-1.8.tar.gz \
 && tar xzf apl-1.8.tar.gz \
 && cd apl-1.8 \
 # Replace stale config.sub/guess with the autotools-shipped ones that know aarch64.
 && cp /usr/share/misc/config.sub /usr/share/misc/config.guess buildtag/ 2>/dev/null || true \
 && cp /usr/share/automake-*/config.sub config.sub \
 && cp /usr/share/automake-*/config.guess config.guess \
 # GNU APL 1.8 has -Werror enabled; GCC 12 flags a stringop-overflow
 # warning in Quad_FIO.cc that stops the build. Disable -Werror.
 && CXXFLAGS="-O2 -Wno-error" CFLAGS="-O2 -Wno-error" \
    ./configure --prefix=/usr/local \
 && make -j && make install

FROM python:3.11-slim
# t64-suffixed names are the post-time_t-transition package names on
# newer Debian bases; pcre3 was replaced by pcre2.
RUN apt-get update && apt-get install -y --no-install-recommends \
      libreadline8t64 libncurses6 libpcre2-8-0 libsqlite3-0 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /usr/local /usr/local
COPY src/ /opt/engine/
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-apl-codex54" eval2.tier="B"
ENTRYPOINT ["python3", "-u", "scripts/uci_proxy.py", "--apl-bin", "apl", "--apl-script", "src/apl/engine.apl"]
