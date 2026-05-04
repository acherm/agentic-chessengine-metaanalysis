# Engine image template for eval2/.
#
# Each engine gets its own subdirectory under docker/engines/<name>/ with:
#   - Dockerfile (this file, customized)
#   - .dockerignore (optional)
#
# Conventions every engine image must follow:
#
#   1. Source is COPYed from the host repo by `runners/build_images.sh`,
#      which mounts the repo at /src/<engine-name> at build time. The
#      Dockerfile receives ENGINE_REPO as a build arg.
#
#   2. Final image's ENTRYPOINT speaks UCI on stdin/stdout, exits cleanly
#      on `quit`, and dies on SIGTERM within 5 s.
#
#   3. WORKDIR at runtime is the engine root (cmd from manifest is run from
#      there).
#
#   4. Apply CPU and memory caps at `docker run` time, not in the Dockerfile.
#      The runners pass --cpus=1 --memory=512m by default; raise per-engine
#      via manifest if justified.
#
#   5. LABEL the image with eval2.* metadata so we can audit later.
#
# This template uses Debian slim; swap base image as needed (e.g.,
# rust:1.79 for Rust engines, eclipse-temurin:21-jre for Java, etc.).

FROM debian:bookworm-slim

ARG ENGINE_NAME=engine
ARG ENGINE_VERSION=unknown

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Source is copied by the build script (see runners/build_images.sh).
COPY src/ /opt/engine/

WORKDIR /opt/engine

# Build step (override per engine).
# RUN make

LABEL eval2.role="engine" \
      eval2.engine="${ENGINE_NAME}" \
      eval2.version="${ENGINE_VERSION}"

# Override ENTRYPOINT per engine to run the UCI binary at PID 1.
# Example: ENTRYPOINT ["./engine"]
ENTRYPOINT ["/bin/sh", "-c", "echo 'TODO: set ENTRYPOINT per engine' >&2; exit 1"]
