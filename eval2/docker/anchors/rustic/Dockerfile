# Rustic — native-UCI Rust engine by Marcel Vanthoor.
# CCRL 40/4 ≈ 1820 (Rustic Alpha 3). Used as the low-mid anchor
# (replaces TSCP 1.81, which speaks xboard v1 only and is incompatible
# with any modern xboard→UCI adapter).
#
# Build:
#   docker build -t eval2/anchor-rustic docker/anchors/rustic/

FROM rust:latest AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
# Pin to Alpha 3.0.4 — the tagged release with published CCRL 40/4 = 1820.
# Do NOT track master: codeberg's master is a 3.99.x pre-v4 build that
# is likely 150–300 Elo stronger than the CCRL-rated Alpha 3.0.4.
RUN git clone --depth 1 --branch alpha-3.0.4 https://codeberg.org/mvanthoor/rustic.git \
 || git clone --depth 1 --branch v3.0.4 https://codeberg.org/mvanthoor/rustic.git \
 || git clone --depth 1 --branch 3.0.4 https://codeberg.org/mvanthoor/rustic.git
WORKDIR /src/rustic
RUN cargo build --release \
 && (strip target/release/rustic 2>/dev/null \
     || strip target/release/rustic-alpha 2>/dev/null \
     || true) \
 && cp target/release/rustic-alpha target/release/rustic 2>/dev/null || true

FROM debian:bookworm-slim
COPY --from=build /src/rustic/target/release/rustic /usr/local/bin/rustic
LABEL eval2.role="anchor" eval2.kind="external" eval2.engine="rustic" eval2.ccrl_40_4="1820"
ENTRYPOINT ["/usr/local/bin/rustic"]
