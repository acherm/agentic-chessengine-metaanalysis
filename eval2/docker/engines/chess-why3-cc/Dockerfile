# chess-why3-cc — Tier B. Why3 extracted to OCaml (NOT to C, despite the
# repo name; "cc" here = Claude Code). Extracted .ml is committed under
# extract/, so we skip the why3-extract step and only run dune.
FROM ocaml/opam:debian-12-ocaml-5.1 AS build
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgmp-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
USER opam
COPY --chown=opam:opam src/ /opt/engine/
WORKDIR /opt/engine
RUN opam install --yes dune zarith \
 && eval $(opam env) \
 && dune build \
 && find _build -name '*.exe' -not -path '*/tests/*' -exec cp {} engine \; -quit \
 && test -x engine

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libgmp10 && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/engine/engine /usr/local/bin/engine
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-why3-cc" eval2.tier="B"
ENTRYPOINT ["/usr/local/bin/engine"]
