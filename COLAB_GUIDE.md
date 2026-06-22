# Running the MOSS @ COLM 2026 notebook on Google Colab

This guide walks through opening and running `moss_pigrpo_probe.ipynb` (and the
exact Table-2 GRPO script `run_grpo_local.py`) on Google Colab, including the
free-tier path the MOSS Colab track requires.

Repo (public): https://github.com/arunshar/moss-pigrpo
Notebook: `moss_pigrpo_probe.ipynb`  |  GRPO script: `run_grpo_local.py`

> Double-blind note: do NOT paste this repo URL into the OpenReview paper or the
> submitted notebook. Upload the anonymized notebook/zip to OpenReview instead.
> A public repo is fine; linking it from the submission is what would deanonymize you.

---

## Part A. Open the notebook in Colab (pick one)

**Method 1, open straight from GitHub (easiest now that the repo is public):**
1. Go to https://colab.research.google.com and sign in.
2. Menu: `File -> Open notebook -> GitHub` tab.
3. In the search box type `arunshar/moss-pigrpo` and press Enter.
4. Click `moss_pigrpo_probe.ipynb`. It opens in Colab.

**Method 2, upload the file:**
1. https://colab.research.google.com -> in the popup choose the `Upload` tab.
2. `Browse` -> select `moss_pigrpo_probe.ipynb` from your computer -> open.

**Method 3, via Google Drive:** drag the `.ipynb` into drive.google.com, then in
Colab `File -> Open notebook -> Google Drive` tab and select it.

---

## Part B. Turn on the GPU (only the GRPO cell needs it)
1. Menu: `Runtime -> Change runtime type`.
2. Hardware accelerator -> `T4 GPU` (free tier is enough). On Colab Pro pick `L4`
   or `A100` for speed. Click `Save`.
3. The reward-hacking probe is pure CPU, so for that alone you can leave it on CPU.

---

## Part C. Run it

**Quickest path (one cell):** the very first code cell is `ONE-CLICK: reproduce
BOTH tables`. Set a T4 GPU (Part B), run that single cell, and it clones the repo,
installs deps, and prints both Table 1 and Table 2 with no uploads. The steps below
are the full cell-by-cell walkthrough if you would rather run the inline study.

1. `Runtime -> Run all` (or press the play button on each cell, top to bottom).
2. What to expect, cell by cell:
   - pip-install cell: installs `transformers` / `torch` (about 1 minute). Safe to rerun.
   - S-KBM + reward cell: defines the kinematic envelope and the hybrid reward (instant).
   - Probe cell (the main claim): prints the table
     `preference-only (w_hard=0) -> +10.0, 0/5` and
     `physics-grounded (w_hard=5) -> -490.5, 5/5`. No GPU needed.
   - GRPO cell: downloads Qwen2.5-0.5B (about 1 GB, a minute), runs the short GRPO,
     and shows the hard-violation rate dropping. A few minutes on a T4; skips with a
     message if on CPU.
   - FLOP-budget + results cell: writes `results.json` and prints the FLOP estimate
     (well under the 1e20 cap).
3. If a cell errors on a fresh runtime, do `Runtime -> Restart and run all` once
   (first-run import quirks).

---

## Part D. Reproduce Table 2 exactly (the measured GRPO numbers)
The notebook's GRPO cell is a demonstration; the exact Table-2 numbers
(preference-only 0.58 -> 1.00, physics 0.50 -> 0.00) come from `run_grpo_local.py`.

Option 1, clone the repo inside Colab (new code cell):
```
!git clone https://github.com/arunshar/moss-pigrpo.git
%cd moss-pigrpo
!pip -q install torch transformers accelerate
!STEPS=50 WHARDS=0.0,5.0 python run_grpo_local.py
```
On a GPU runtime it uses the GPU automatically. To force CPU, prefix `FORCE_CPU=1`.
It prints `base` / `trained` hard-violation rates and writes `grpo_results_all.json`.

Option 2, upload `run_grpo_local.py` via the Files sidebar (left, folder icon ->
Upload), then run `!STEPS=50 WHARDS=0.0,5.0 python run_grpo_local.py`.

---

## Part E. Save the executed notebook for submission
1. After everything has run (outputs visible), `File -> Download -> Download .ipynb`.
   The saved copy carries the printed outputs, which is what MOSS reviewers run.
2. To grab `results.json`: Files sidebar -> hover the file -> three-dot menu -> `Download`.
3. For OpenReview: upload the executed `.ipynb` (and a zip of the code if you want),
   anonymized. The MOSS FAQ says reviewers judge the paper by running this notebook,
   so make sure the probe cell runs cleanly on free-tier Colab (it does, it is CPU-only).

---

## Free-tier and timing
- The probe is free-tier reproducible (CPU, no downloads, seconds).
- The 0.5B GRPO fits a free T4 GPU in a few minutes, well within the MOSS Colab-track
  limits (<= 1 GPU, <= 12 h, <= 500 GB).
- Colab Pro only makes it faster; nothing here requires it.
