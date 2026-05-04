# Asymptote 0.7 — native-UCI Rust engine by Maximilian Lupke.
# CCRL 40/4 ≈ 2150. Used as the mid anchor.

FROM rust:latest AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch v0.7 https://github.com/malu/asymptote.git \
 || git clone --depth 1 https://github.com/malu/asymptote.git
WORKDIR /src/asymptote
RUN cargo build --release && strip target/release/asymptote

FROM debian:bookworm-slim
COPY --from=build /src/asymptote/target/release/asymptote /usr/local/bin/asymptote
LABEL eval2.role="anchor" eval2.kind="external" eval2.engine="asymptote" eval2.ccrl_40_4="2150"
ENTRYPOINT ["/usr/local/bin/asymptote"]
