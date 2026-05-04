"""Scatter plot: round-robin Elo (y) vs Phase B anchor Elo (x).
Engines bounded in Phase B (only floor stamp) are drawn open-circle to
indicate the x-coordinate is an upper-bound proxy, not a measurement.
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
import matplotlib.pyplot as plt  # noqa: E402
from score_rr import parse_all, fit_elo, PHASE_B  # noqa: E402

# Engines whose Phase B value is the saturation floor (not a real measurement).
PHASE_B_BOUNDED = {
    "chess-purec-codex", "chess-ruby-codex", "chess-ruby-cc", "chess-py",
    "chess-py-cc", "chess-cobol-cc", "COBOL-chess", "chess-why3", "lean-chess",
    "chess-apl-codex54", "chess-icon-codex", "chess-latex-codex-replication",
}

results = parse_all()
rr_elos = fit_elo(results)

# Build (x_phaseb, y_rr, label, bounded?) tuples
rows = []
for e, rr in rr_elos.items():
    if e not in PHASE_B: continue
    rows.append((PHASE_B[e], rr, e, e in PHASE_B_BOUNDED))

fig, ax = plt.subplots(figsize=(11, 8))
xs_meas, ys_meas, xs_bnd, ys_bnd = [], [], [], []
for x, y, name, bounded in rows:
    (xs_bnd if bounded else xs_meas).append(x)
    (ys_bnd if bounded else ys_meas).append(y)
    ax.annotate(name, (x, y), xytext=(4, 4), textcoords="offset points",
                fontsize=8, color=("gray" if bounded else "black"))

ax.scatter(xs_meas, ys_meas, marker="o", s=70, label="Phase B measured (Elo from anchors)",
           color="C0", edgecolor="black", linewidths=0.5, zorder=3)
ax.scatter(xs_bnd, ys_bnd, marker="o", s=70, facecolor="white",
           edgecolor="C0", linewidths=1.2, zorder=3,
           label="Phase B bounded (anchor saturated; x is floor)")

# y = x reference
xmin = min(min(xs_meas), min(xs_bnd)) - 50
xmax = max(max(xs_meas), max(xs_bnd)) + 50
ymin = min(rr_elos.values()) - 50
ymax = max(rr_elos.values()) + 50
lo, hi = min(xmin, ymin), max(xmax, ymax)
ax.plot([lo, hi], [lo, hi], "--", color="gray", linewidth=1, label="y = x (perfect agreement)")

ax.set_xlabel("Phase B anchor-based Elo", fontsize=12)
ax.set_ylabel("Round-robin Elo (Bradley-Terry MLE, anchored to chess-rust-cc-redo @ 1989)",
              fontsize=12)
ax.set_title("23-engine corpus: round-robin Elo vs Phase B anchor Elo\n"
             "(253 pairs, 506 games at TC=120+1)", fontsize=13)
ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
ax.grid(alpha=0.3)
ax.legend(loc="lower right", fontsize=10)

# Stats annotation
import statistics as stat
xs_all = [r[0] for r in rows]; ys_all = [r[1] for r in rows]
mx, my = stat.mean(xs_all), stat.mean(ys_all)
num = sum((x - mx) * (y - my) for x, y in zip(xs_all, ys_all))
den = (sum((x - mx) ** 2 for x in xs_all) * sum((y - my) ** 2 for y in ys_all)) ** 0.5
pearson = num / den
rxs = [sorted(xs_all).index(x) for x in xs_all]
rys = [sorted(ys_all).index(y) for y in ys_all]
mx, my = stat.mean(rxs), stat.mean(rys)
num = sum((a - mx) * (b - my) for a, b in zip(rxs, rys))
den = (sum((a - mx) ** 2 for a in rxs) * sum((b - my) ** 2 for b in rys)) ** 0.5
spearman = num / den

# Pearson on the measured-only subset (no floor-stamped)
xs_m = [r[0] for r in rows if not r[3]]; ys_m = [r[1] for r in rows if not r[3]]
mx2, my2 = stat.mean(xs_m), stat.mean(ys_m)
num2 = sum((x - mx2) * (y - my2) for x, y in zip(xs_m, ys_m))
den2 = (sum((x - mx2) ** 2 for x in xs_m) * sum((y - my2) ** 2 for y in ys_m)) ** 0.5
pearson_m = num2 / den2

ax.text(0.02, 0.98,
        f"All n={len(rows)}:  Pearson r = {pearson:.3f},  Spearman ρ = {spearman:.3f}\n"
        f"Measured-only n={len(xs_m)}:  Pearson r = {pearson_m:.3f}",
        transform=ax.transAxes, ha="left", va="top", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="gray", alpha=0.9))

out = Path("results/rr_vs_phaseb.png")
out.parent.mkdir(parents=True, exist_ok=True)
plt.tight_layout()
plt.savefig(out, dpi=140)
print(f"wrote {out}")
print(f"all (n={len(rows)}): pearson={pearson:.3f}  spearman={spearman:.3f}")
print(f"measured-only (n={len(xs_m)}): pearson={pearson_m:.3f}")
