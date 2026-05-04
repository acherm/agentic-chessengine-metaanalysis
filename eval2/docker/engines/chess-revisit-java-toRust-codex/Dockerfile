# chess-revisit-java-toRust-codex — Java→Rust port (special-role).
# Cargo package name is chess_engine_rust; binary is typically
# target/release/chess_engine_rust (Cargo replaces underscores? no —
# package `chess_engine_rust` yields binary `chess_engine_rust`).
FROM rust:1.85-bookworm AS build
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN cargo build --release \
 && cp target/release/chess_engine_rust target/release/engine 2>/dev/null \
    || cp target/release/chess-engine-rust target/release/engine 2>/dev/null \
    || (cd target/release && ls -1 | grep -vE '\.(d|rmeta|rlib)$' | head -1 | xargs -I{} cp {} engine) \
 && test -x target/release/engine

FROM debian:bookworm-slim
COPY --from=build /opt/engine/target/release/engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-revisit-java-torust-codex" eval2.tier="A" \
      eval2.flag="port-special-role"
ENTRYPOINT ["/usr/local/bin/engine"]
