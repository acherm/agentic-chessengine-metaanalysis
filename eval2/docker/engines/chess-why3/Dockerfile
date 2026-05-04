# chess-why3 — Tier B. Why3 extracted to OCaml + dune.
# Executable lives at _build/default/src/uci_ocaml/main.exe (per repo dune file).
FROM ocaml/opam:debian-12-ocaml-5.1 AS build
# zarith needs libgmp-dev + pkg-config; install as root before dropping back.
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgmp-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
USER opam
COPY --chown=opam:opam src/ /opt/engine/
WORKDIR /opt/engine
RUN opam install --yes dune zarith \
 && eval $(opam env) \
 && (dune build src/uci_ocaml/main.exe || dune build) \
 && find _build -name 'main.exe' -exec cp {} engine \; -quit \
 && test -x engine

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libgmp10 && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/engine/engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-why3" eval2.tier="B"
ENTRYPOINT ["/usr/local/bin/engine"]
