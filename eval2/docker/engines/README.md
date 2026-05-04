# Engine container images

One subdirectory per engine in `manifest.yaml`. Each has a `Dockerfile`
that produces a self-contained UCI image.

## How `build_images.sh` calls these

For each engine, the runner:

1. Rsyncs the engine repo (from `path:` in `manifest.yaml`) into a
   throwaway build context at `<tmpdir>/src/`.
2. Copies the engine's `Dockerfile` (this directory) into the same
   context.
3. Runs `docker build -t <image> --build-arg ENGINE_VERSION=<sha> .`.

So inside any engine Dockerfile, sources are reliably at `src/`.

## Status

- `_template/` — base template, do not build.
- `chess-rust-cc/` — done (Tier A example).
- `chess-java-cc/` — done (Tier B example).
- `chess-latex-codex-replication/` — done (Tier C example, heaviest).
- All other engines listed in `manifest.yaml` need their own Dockerfile
  added here. Until then, those engines will be skipped by
  `runners/build_images.sh` and reported in `results/missing.txt`.

## Conventions to follow when adding a new engine

- ENTRYPOINT speaks UCI on stdin/stdout (no shell wrapper if avoidable).
- Final image stays under ~500 MB except for Tier C (LaTeX needs ~1 GB).
- No build artifacts in the final image (multi-stage builds).
- LABEL the image with at least `eval2.role`, `eval2.engine`, `eval2.tier`.
- Don't bake CPU/memory caps into the image — the runner sets them.
- If the engine wraps an interpreter (python/ruby/dyalog/mojo), make sure
  PID 1 is the interpreter, not a shell, so SIGTERM kills it cleanly.
