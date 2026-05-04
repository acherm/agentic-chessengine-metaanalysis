# chess-rust-codex — Tier A. Uses Rust edition 2024 (Cargo.toml), so
# we need rust >= 1.85. Uses the `chess` crate for board types.
FROM rust:1.85-bookworm AS build
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN cargo build --release && strip target/release/rust_chess_engine 2>/dev/null \
 || strip target/release/engine 2>/dev/null \
 || true

FROM debian:bookworm-slim
# Cargo names the binary after the `name` in Cargo.toml: rust_chess_engine.
COPY --from=build /opt/engine/target/release/rust_chess_engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-rust-codex" eval2.tier="A"
ENTRYPOINT ["/usr/local/bin/engine"]
