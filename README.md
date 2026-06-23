# Pi-GRPO: Physics as a Hard Reward Floor

## Overview
**Pi-GRPO** studies an **unbounded hard physics-violation reward term** as a structural
defense against reward hacking in reinforcement-learning post-training. When a reward
scores only the surface form of a completion, a fluent but physically impossible output
can be rewarded by a rater yet is operationally wrong. Pi-GRPO adds an unbounded penalty
on physical-law violations so that a single sustained violation dominates any bounded
preference signal, giving the reward a floor that no preference score can lift a violating
completion above. The same reward plugs into **PPO, DPO, and GRPO**. This repository
reproduces the paper's two headline results at small scale, under 10^15 FLOPs, in a free
Google Colab notebook.

## Key Contributions
- **Unbounded hard reward floor:** a physics-violation penalty that is never clipped, with
  a dominance argument showing one violation cannot be outweighed by any bounded preference term.
- **Model-free reward-hacking probe:** a CPU-only diagnostic that isolates the failure and
  its fix without training or a large model.
- **One reward, three trainers:** a single reward surface shared by PPO, DPO, and GRPO.
- **Small-scale reproducibility:** a measured GRPO run on Qwen2.5-0.5B-Instruct and a
  free-Colab notebook, all under the workshop compute budget.

## Requirements
Pi-GRPO is implemented in **Python (>=3.9)** and **PyTorch**. Key dependencies:
```
python>=3.9
torch
transformers
accelerate
numpy
```

## Installation
```
git clone https://github.com/arunshar/moss-pigrpo.git
cd moss-pigrpo
pip install torch transformers accelerate
```

## Reproducing the Results

### Table 1: reward-hacking probe (CPU, seconds)
```
python run_probe.py
```
Scores a preference-only reward against the physics-grounded reward on feasible and
infeasible completions, prints the mean reward and catch rate, and writes `probe_results.json`.

### Table 2: small-scale GRPO (Qwen2.5-0.5B-Instruct)
```
STEPS=40 WHARDS=0.0,5.0 python run_grpo_local.py
```
Runs GRPO under two reward configurations and reports the hard-violation rate before and
after training. Uses a GPU when one is present and falls back to CPU.

### Google Colab
Open `moss_pigrpo_probe.ipynb` in Colab, set a **T4 GPU**, and run the first cell; it
installs the dependencies and reproduces both tables. See `COLAB_GUIDE.md` for the
step-by-step free-tier path.

## Results
Table 1, reward-hacking probe:
```
preference-only  (w_hard=0):  +10.0    0/5 caught
physics-grounded (w_hard=5):  -490.5   5/5 caught
```
Table 2, small-scale GRPO (hard-violation rate, before -> after training):
```
preference-only  (w_hard=0):  0.58 -> 1.00   (training hacks the reward)
physics-grounded (w_hard=5):  0.50 -> 0.00   (the floor drives violations to zero)
```

## Repository Structure
```text
moss-pigrpo/
├── paper.tex / paper.pdf       # the 4-page paper (ICML / MOSS style)
├── moss.bib                    # references
├── moss_pigrpo_probe.ipynb     # Colab notebook: first cell reproduces both tables
├── run_probe.py                # Table 1, model-free reward-hacking probe (CPU)
├── run_grpo_local.py           # Table 2, small-scale GRPO on Qwen2.5-0.5B
├── probe_results.json          # saved Table 1 output
├── grpo_results.json           # saved Table 2 outputs
├── COLAB_GUIDE.md              # detailed Colab walkthrough
└── README.md                   # this file
```

## Citation
If you use this work, please cite:
```bibtex
@inproceedings{sharma2026pigrpo,
  title     = {Physics as a Hard Reward Floor: A Small-Scale, Controlled Study of
               Reward-Hacking Mitigation in RL Post-Training},
  author    = {Sharma, Arun},
  booktitle = {Methods and Opportunities at Small Scale (MOSS), Workshop at COLM},
  year      = {2026},
  note      = {Under review}
}
```
