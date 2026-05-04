# chess-rust-cc — Tier A, native-fast Rust engine.
# Build: docker build --build-arg ENGINE_VERSION=$(date +%Y%m%d) \
#          -t eval2/chess-rust-cc:latest \
#          -f docker/engines/chess-rust-cc/Dockerfile .
# (build context is repo root; src/ is rsynced in by build_images.sh)

FROM rust:1.79-bookworm AS build
ARG ENGINE_VERSION=unknown
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN cargo build --release && strip target/release/chess-engine

FROM debian:bookworm-slim
COPY --from=build /opt/engine/target/release/chess-engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-rust-cc" eval2.tier="A"
ENTRYPOINT ["/usr/local/bin/engine"]
