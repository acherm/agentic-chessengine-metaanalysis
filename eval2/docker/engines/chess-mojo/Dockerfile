# chess-mojo — Tier B (failure-class). Mojo from Modular.
#
# !!! Mojo's official image lives at modular/max:nightly and requires a
# Modular auth token at build time for some installs. The Community
# image works for `mojo run` but you may need to accept their EULA.
# If unavailable, this engine is excluded.

FROM modular/max:24.5.0
COPY src/ /opt/engine/
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-mojo" eval2.tier="B" \
      eval2.flag="failure-case"
ENTRYPOINT ["mojo", "run", "src/mojo_engine/main.mojo"]
