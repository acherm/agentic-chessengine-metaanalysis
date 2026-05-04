"""Trivial UCI random-legal-move engine.

Used as a baseline for Tier-C engines. Plays a uniformly random legal
move on every turn. Requires python-chess.

Run: python3 lib/random_mover.py
"""
from __future__ import annotations

import random
import sys

import chess


def main() -> None:
    board = chess.Board()
    rng = random.Random(20260419)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if line == "uci":
            print("id name eval2-random-mover")
            print("id author eval2")
            print("uciok", flush=True)
        elif line == "isready":
            print("readyok", flush=True)
        elif line == "ucinewgame":
            board = chess.Board()
        elif line.startswith("position"):
            board = _apply_position(line)
        elif line.startswith("go"):
            moves = list(board.legal_moves)
            if not moves:
                print("bestmove 0000", flush=True)
            else:
                mv = rng.choice(moves)
                print(f"bestmove {mv.uci()}", flush=True)
        elif line == "quit":
            return


def _apply_position(line: str) -> chess.Board:
    parts = line.split()
    i = 1
    if i < len(parts) and parts[i] == "startpos":
        b = chess.Board()
        i += 1
    elif i < len(parts) and parts[i] == "fen":
        fen = " ".join(parts[i + 1:i + 7])
        b = chess.Board(fen)
        i += 7
    else:
        return chess.Board()
    if i < len(parts) and parts[i] == "moves":
        for mv in parts[i + 1:]:
            try:
                b.push_uci(mv)
            except Exception:
                break
    return b


if __name__ == "__main__":
    main()
