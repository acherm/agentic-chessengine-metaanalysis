# chess-Rocq — Tier B. OCaml binary extracted from a Rocq (Coq) proof.
# Per session logs: needs opam switch on OCaml 5.2.1 + rocq.9.1.0 package.
# (Our earlier attempt installed "rocq-runtime" alone, which is only the
# runtime lib; the full `rocq` package provides the compiler the proofs
# need to extract OCaml from.)
FROM ocaml/opam:debian-12-ocaml-5.2 AS build
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgmp-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
USER opam
COPY --chown=opam:opam src/ /opt/engine/
WORKDIR /opt/engine
RUN opam update \
 && (opam install --yes rocq.9.1.0 zarith dune \
     || opam install --yes coq.8.19.0 zarith dune) \
 && eval $(opam env) && dune build \
 && find _build -name 'main.exe' -exec cp {} engine \; -quit \
 && test -x engine

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libgmp10 && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/engine/engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-Rocq" eval2.tier="B"
ENTRYPOINT ["/usr/local/bin/engine"]
