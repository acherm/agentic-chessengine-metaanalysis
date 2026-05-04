# chess-rust-cc-redo — Tier A. CC-built Rust engine, from-scratch redo
# (no `chess` crate, no external deps) to address the evasion concern that
# chess-rust-codex raised. Cargo package is `chess_engine`.
FROM rust:1.85-bookworm AS build
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN cargo build --release && strip target/release/chess_engine

FROM debian:bookworm-slim
COPY --from=build /opt/engine/target/release/chess_engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-rust-cc-redo" eval2.tier="A"
ENTRYPOINT ["/usr/local/bin/engine"]
