#!/usr/bin/env python3
"""Produce a double-blind anonymized copy of this repository.

The source repo is authored under a real GitHub handle and name. For MOSS @ COLM
2026 (double-blind via OpenReview) we need a copy with every author identifier
removed from the *content*. This script is deterministic: given the same source
tree it always emits the same anonymized tree, so it can run unattended inside a
GitHub Action on every push to keep an anonymized mirror in sync.

What it does
  1. Copies the publishable files into an output tree.
  2. Rewrites the few files that name the author's GitHub handle:
       - the notebook's one-click cell  -> runs from uploaded files, no clone
       - COLAB_GUIDE.md                 -> a clean upload-and-run guide
       - README.md                      -> an anonymized banner + safety scrub
  3. Excludes anything that would leak identity or the sync mechanism
     (.git, .github/, scripts/, build outputs, LaTeX aux files).
  4. With --check, scans the output tree and exits non-zero if any banned
     identifier survived. Citation co-authors (e.g. "Archit Sharma" in moss.bib)
     are legitimate and are never touched, because we only scrub the exact handle
     token and the author's own name, not the substring "Sharma".

Usage
  python3 scripts/anonymize.py --src . --out build/anon      # build the tree
  python3 scripts/anonymize.py --check build/anon            # verify it is clean

House rule: no em dashes anywhere, including comments.
"""
import argparse
import json
import os
import re
import shutil
import sys

# The exact author identifiers to scrub from content. We match the GitHub handle
# token and the full personal name / email, never the bare surname (which also
# appears as a legitimate citation co-author).
HANDLE = "arunshar"
BANNED = [
    HANDLE,
    "Arun Sharma",
    "arun08sharma",
    "sharm485",
    "umn.edu",
]

# Files copied verbatim (already verified blind: the PDF metadata is
# "Anonymous Authors" and the .tex front matter is "Anonymous Author(s)").
VERBATIM = [
    "paper.tex", "paper.pdf", "moss.bib",
    "icml2025.sty", "MOSS_camera_ready.sty", "icml2025.bst",
    "fancyhdr.sty", "algorithm.sty", "algorithmic.sty",
    "example_paper.tex", "example_paper.bib",
    "run_probe.py", "run_grpo_local.py",
    "grpo_results.json", "grpo_results_phys.json", "probe_results.json",
    ".gitignore",
]

ANON_README = """# Physics as a Hard Reward Floor: reproduction package

> Anonymized copy for double-blind review (MOSS @ COLM 2026). Author and citation
> details are omitted. Run the code from the uploaded supplementary files; there is
> no public repository to clone here.

## Overview
An unbounded hard penalty on physical-law violations gives a reinforcement-learning
post-training reward a floor that no bounded preference signal can lift a violating
completion above. The same reward plugs into PPO, DPO, and GRPO. This package
reproduces the two headline results at small scale, under 10^15 FLOPs, in a free
Google Colab notebook:

- Table 1: a model-free reward-hacking probe (CPU, seconds).
- Table 2: a small-scale GRPO run on Qwen2.5-0.5B-Instruct (one GPU, a few minutes).

## Requirements
Python (>= 3.9) with `torch`, `transformers`, `accelerate`, and `numpy`. The probe
needs only NumPy and runs on CPU.

## Reproduce in Google Colab
1. Go to https://colab.research.google.com and choose **File -> Upload notebook**,
   selecting `moss_pigrpo_probe.ipynb`.
2. Open the **Files** sidebar and upload `run_probe.py` and `run_grpo_local.py` next
   to the notebook (or unzip the supplement).
3. **Runtime -> Change runtime type -> T4 GPU**, then **Save** (Table 1 is CPU-only).
4. Run the first cell, "ONE-CLICK: reproduce BOTH tables". It installs the
   dependencies and runs both scripts end to end.

## Reproduce locally
```
pip install torch transformers accelerate
python run_probe.py                              # Table 1 (CPU, seconds)
STEPS=40 WHARDS=0.0,5.0 python run_grpo_local.py # Table 2 (uses a GPU if present)
```

## Results
Table 1, reward-hacking probe:
```
preference-only  (w_hard=0):  +10.0    0/5 caught
physics-grounded (w_hard=5):  -490.5   5/5 caught
```
Table 2, small-scale GRPO (hard-violation rate, before -> after training):
```
preference-only  (w_hard=0):  0.58 -> 1.00
physics-grounded (w_hard=5):  0.50 -> 0.00
```

## Repository structure
```text
.
|-- moss_pigrpo_probe.ipynb   # Colab notebook: first cell reproduces both tables
|-- run_probe.py              # Table 1, model-free reward-hacking probe (CPU)
|-- run_grpo_local.py         # Table 2, small-scale GRPO on Qwen2.5-0.5B
|-- probe_results.json        # saved Table 1 output
|-- grpo_results.json         # saved Table 2 output
`-- COLAB_GUIDE.md            # detailed Colab walkthrough
```

## Citation
Omitted for double-blind review.
"""

# A clean, upload-based one-click cell for the anonymized notebook. No clone URL.
ANON_ONECLICK = (
    '#@title  ONE-CLICK: reproduce BOTH tables  (run from the uploaded files)  { display-mode: "form" }\n'
    "# Anonymized copy for double-blind review.\n"
    "# Put run_probe.py and run_grpo_local.py next to this notebook\n"
    "# (Colab: Files sidebar -> Upload, or unzip the supplement here), then:\n"
    "#   1) Runtime -> Change runtime type -> T4 GPU (free tier is enough), Save.\n"
    "#   2) Run THIS cell. It installs deps and runs both scripts. Nothing to clone.\n"
    "import os, sys, subprocess\n"
    "\n"
    "def sh(cmd):\n"
    '    print("\\n$ " + cmd, flush=True)\n'
    "    subprocess.run(cmd, shell=True, check=False)\n"
    "\n"
    'print(">>> installing deps (a no-op if already present on Colab) ...", flush=True)\n'
    'sh(sys.executable + " -m pip -q install torch transformers accelerate")\n'
    "\n"
    'need = [f for f in ("run_probe.py", "run_grpo_local.py") if not os.path.exists(f)]\n'
    "if need:\n"
    '    print("Missing files: " + ", ".join(need))\n'
    '    print("Upload them (Files sidebar -> Upload) or unzip the supplement here, then re-run.")\n'
    "else:\n"
    '    print("\\n" + "#" * 64)\n'
    '    print("# TABLE 1: reward-hacking probe  (model-free, CPU, under a second)")\n'
    '    print("#" * 64, flush=True)\n'
    '    sh(sys.executable + " run_probe.py")\n'
    '    print("\\n" + "#" * 64)\n'
    '    print("# TABLE 2: small-scale GRPO on Qwen2.5-0.5B  (uses the GPU if present)")\n'
    '    print("#" * 64, flush=True)\n'
    '    sh("STEPS=40 WHARDS=0.0,5.0 " + sys.executable + " run_grpo_local.py")\n'
    '    print("\\n>>> done.")\n'
    '    print(">>> Table 1 expected:  preference-only +10.0 (0/5)  vs  physics -490.5 (5/5).")\n'
    '    print(">>> Table 2 expected:  base vs trained hard-violation rate for w_hard=0 and w_hard=5.")\n'
)

ANON_COLAB_GUIDE = """# Running the MOSS @ COLM 2026 notebook on Google Colab (anonymized)

> Anonymized copy for double-blind review. There is no repository to clone; run
> from the supplementary files uploaded with the submission.

The supplement contains `moss_pigrpo_probe.ipynb`, `run_probe.py`, and
`run_grpo_local.py`. The reward-hacking probe (Table 1) is pure CPU; the small
GRPO run (Table 2) uses one GPU.

## A. Open the notebook
1. Go to https://colab.research.google.com and sign in.
2. `File -> Open notebook -> Upload` and select `moss_pigrpo_probe.ipynb`.

## B. Upload the two scripts next to it
1. Open the Files sidebar (folder icon on the left).
2. `Upload to session storage` and add `run_probe.py` and `run_grpo_local.py`.
   (Or upload the supplement `.zip` and unzip it in a cell: `!unzip -o supplement.zip`.)

## C. Turn on the GPU (only Table 2 needs it)
1. `Runtime -> Change runtime type -> T4 GPU` (free tier is enough), then `Save`.

## D. Run it
1. Run the first cell, `ONE-CLICK: reproduce BOTH tables`. It installs deps and
   runs both scripts from the uploaded files.
2. Expected output:
   - Table 1: `preference-only (w_hard=0) -> +10.0, 0/5` and
     `physics-grounded (w_hard=5) -> -490.5, 5/5`. No GPU needed.
   - Table 2: base vs trained hard-violation rate for `w_hard=0` and `w_hard=5`
     (preference-only drifts to / stays infeasible; physics drives it to zero).
3. If a cell errors on a fresh runtime, `Runtime -> Restart and run all` once.

## E. Save the executed notebook
`File -> Download -> Download .ipynb` after the outputs are visible. MOSS
reviewers judge the claim by running this notebook, and the probe cell runs on
free-tier CPU in seconds.

## Free-tier and timing
- The probe is free-tier reproducible (CPU, no downloads, seconds).
- The 0.5B GRPO fits a free T4 GPU in a few minutes, within the MOSS Colab-track
  limits (<= 1 GPU, <= 12 h, <= 500 GB).
"""

# Directory / file names never copied into the anonymized tree.
EXCLUDE_DIRS = {".git", ".github", "scripts", "build", "openreview_submission", "__pycache__"}
EXCLUDE_SUFFIX = {".aux", ".log", ".out", ".bbl", ".blg", ".bak"}
EXCLUDE_NAMES = {".DS_Store"}


def anon_readme(src_root):
    # The public README carries author name, GitHub URLs, and a citation block, none
    # of which may appear in the blind mirror. Rather than scrub a moving target, emit
    # a fixed anonymized README written for reviewers. --check is the gate either way.
    return ANON_README


def anon_notebook(src_root):
    """Anonymize the notebook robustly, whatever shape it is in.

    Colab's "Save a copy to GitHub" rewrites the notebook: it adds an Open-In-Colab
    badge that names the repo, bakes in execution outputs, can drop cells, and adds
    a metadata.colab block. So we never depend on a specific cell being present. We
    drop the badge cell, clear every output, strip the Colab metadata, replace the
    clone-based one-click cell with a no-clone version (or inject that cell if it is
    missing), and scrub the handle from any remaining source. The --check pass is
    the final gate, so the build never silently ships an identifier.
    """
    with open(os.path.join(src_root, "moss_pigrpo_probe.ipynb"), encoding="utf-8") as f:
        nb = json.load(f)

    kept = []
    have_oneclick = False
    for cell in nb.get("cells", []):
        src = "".join(cell.get("source", []))
        # Drop the Colab badge cell; it embeds the repo path.
        if cell.get("cell_type") == "markdown" and ("colab-badge.svg" in src or "Open In Colab" in src):
            continue
        # No runtime leaks: clear outputs and execution counts on code cells.
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        # Swap the clone-based one-click cell for the no-clone version; otherwise
        # scrub the handle from whatever source remains.
        if cell.get("cell_type") == "code" and "ONE-CLICK" in src and "git clone" in src:
            cell["source"] = ANON_ONECLICK.splitlines(keepends=True)
            have_oneclick = True
        else:
            cell["source"] = src.replace(HANDLE, "ANONYMOUS").splitlines(keepends=True)
        kept.append(cell)
    nb["cells"] = kept

    # Strip Colab-added notebook metadata (provenance, authorship_tag, name).
    md = nb.get("metadata", {})
    md.pop("colab", None)
    md.pop("widgets", None)

    # If no clone-based one-click cell existed, inject the no-clone one right after
    # the first markdown cell so the convenience path still exists in the mirror.
    if not have_oneclick:
        new_cell = {
            "cell_type": "code", "metadata": {},
            "execution_count": None, "outputs": [],
            "source": ANON_ONECLICK.splitlines(keepends=True),
        }
        pos = 0
        for i, c in enumerate(nb["cells"]):
            if c.get("cell_type") == "markdown":
                pos = i + 1
                break
        nb["cells"].insert(pos, new_cell)

    return json.dumps(nb, indent=1, ensure_ascii=False) + "\n"


def build(src_root, out_root):
    if os.path.exists(out_root):
        shutil.rmtree(out_root)
    os.makedirs(out_root)

    for name in VERBATIM:
        srcp = os.path.join(src_root, name)
        if os.path.exists(srcp):
            shutil.copy2(srcp, os.path.join(out_root, name))

    with open(os.path.join(out_root, "README.md"), "w", encoding="utf-8") as f:
        f.write(anon_readme(src_root))
    with open(os.path.join(out_root, "COLAB_GUIDE.md"), "w", encoding="utf-8") as f:
        f.write(ANON_COLAB_GUIDE)
    with open(os.path.join(out_root, "moss_pigrpo_probe.ipynb"), "w", encoding="utf-8") as f:
        f.write(anon_notebook(src_root))


def check(out_root):
    """Scan the tree; return a list of (file, lineno, line) leaks."""
    leaks = []
    for dirpath, dirnames, filenames in os.walk(out_root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if fn in EXCLUDE_NAMES or os.path.splitext(fn)[1] in EXCLUDE_SUFFIX:
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, out_root)
            try:
                with open(path, "rb") as f:
                    raw = f.read()
            except OSError:
                continue
            # Binary (PDF): scan decoded latin-1 for the banned tokens as bytes.
            text = raw.decode("utf-8", errors="ignore")
            for i, line in enumerate(text.splitlines(), 1):
                for tok in BANNED:
                    if tok in line:
                        leaks.append((rel, i, tok, line.strip()[:120]))
    return leaks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=".")
    ap.add_argument("--out", default="build/anon")
    ap.add_argument("--check", metavar="DIR", help="scan DIR for leaks and exit")
    args = ap.parse_args()

    if args.check:
        leaks = check(args.check)
        if leaks:
            print("ANONYMIZATION CHECK FAILED: identifier(s) found:")
            for rel, i, tok, line in leaks:
                print(f"  {rel}:{i}  [{tok}]  {line}")
            sys.exit(1)
        print(f"anonymization check OK: no banned identifiers in {args.check}")
        return

    build(args.src, args.out)
    leaks = check(args.out)
    if leaks:
        print("BUILD produced leaks (this is a bug in anonymize.py):")
        for rel, i, tok, line in leaks:
            print(f"  {rel}:{i}  [{tok}]  {line}")
        sys.exit(1)
    print(f"anonymized tree written to {args.out} and verified clean")


if __name__ == "__main__":
    main()
