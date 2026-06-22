# MOSS @ COLM 2026 submission (Pi-GRPO: small-scale reward-hacking study)

Workshop: **Methods and Opportunities at Small Scale (MOSS)**, COLM 2026 (Oct 9, 2026).
Submit via **OpenReview**: https://openreview.net/group?id=colmweb.org/COLM/2026/Workshop/MOSS
Workshop deadline June 30 AoE; this is the internal-review draft.

## What it is
A re-scoped, anonymized paper carved out of the Pi-GRPO work: a method (an
**unbounded hard physics-violation reward term**) plus a **controlled diagnosis of
reward hacking**, demonstrated at small scale. Based on **Pi-GRPO only** (not PC-RF,
not the combined paper): PC-RF is off-topic for a language workshop, and the merged
paper is over the 3B cap.

## Status: both internal-review items done
- **Format (item 1):** now in the official **MOSS / ICML-2025 blind template** (style files
  pulled from the workshop Drive folder: `icml2025.sty`, `MOSS_camera_ready.sty`,
  `icml2025.bst`, `fancyhdr.sty`, `algorithm*.sty`). Single-column, anonymized, 4 pages,
  builds clean with bibtex.
- **Measured GRPO (item 2):** real GRPO run on **Qwen2.5-0.5B-Instruct** (laptop GPU/CPU,
  < 1e15 FLOPs, far under the 1e20 cap):
  - Preference-only (w_hard=0): hard-violation rate **0.58 -> 1.00** (training hacks the reward).
  - Physics-grounded (w_hard=5): **0.50 -> 0.00** (the unbounded floor drives violations to zero).

## Files
- `paper.pdf` / `paper.tex` - the 4-page MOSS draft (blind). `moss.bib` - references.
- Style files: `icml2025.sty`, `MOSS_camera_ready.sty`, `icml2025.bst`, `fancyhdr.sty`, `algorithm.sty`, `algorithmic.sty`. `example_paper.tex/.bib` - the official MOSS template, kept for reference.
- `moss_pigrpo_probe.ipynb` - free-Colab notebook: reproduces the reward-hacking probe (the main claim) and a small GRPO demo.
- `run_grpo_local.py` - the GRPO script that produced the measured Table 2 numbers (runs on a laptop in minutes; also runs on Colab). `grpo_results_phys.json` - its output.
- `paper_neurips_standin.tex.bak` - the earlier neurips-format stand-in (superseded).

## Measured vs in-progress (kept honest in the paper)
- **Measured:** the reward-hacking probe (0/5 vs 5/5; +10.0 vs -490.5), the 13/13 guardrail
  tests, the golden-evaluator verdicts, the KL-controller band, the safe-range guard, hot-path
  cost, and the **small-scale GRPO** (Table 2).
- **In progress (flagged, Table 3):** trained-policy rates on a larger model.

## Before camera-ready (after June 30 acceptance)
1. Switch the blind line `\usepackage{icml2025}` to `\usepackage[accepted]{MOSS_camera_ready}`, add author info, and use the one extra page allowed.
2. Optionally fold `run_grpo_local.py` directly into the notebook so a single "Run all" reproduces Table 2 (FAQ Q4/Q6: reviewers judge by the notebook; you may import from code files).

## Build
`pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper` (style files are in this folder).
