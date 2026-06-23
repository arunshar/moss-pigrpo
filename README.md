# Physics as a Hard Reward Floor: reproduction package (MOSS @ COLM 2026)

This package reproduces the two headline results of the paper:
- **Table 1**, a model-free reward-hacking probe (CPU, seconds).
- **Table 2**, a small-scale GRPO run on Qwen2.5-0.5B-Instruct (one GPU, a few minutes).

Everything runs in a free Google Colab notebook under 10^15 FLOPs, far below the 10^20 cap.

## Reproduce in Google Colab (step by step)

1. Go to https://colab.research.google.com and sign in.
2. **File -> Upload notebook** and choose `moss_pigrpo_probe.ipynb`.
3. Open the **Files** sidebar (the folder icon on the left) and upload `run_probe.py`
   and `run_grpo_local.py` next to the notebook. (Or upload the whole supplement and
   unzip it in a cell with `!unzip -o supplement.zip`.)
4. **Runtime -> Change runtime type -> T4 GPU** (the free tier is enough), then **Save**.
   Table 1 is CPU-only, so you can skip this if you only want the probe.
5. Run the **first cell** ("ONE-CLICK: reproduce BOTH tables"). It installs the
   dependencies and runs both scripts end to end. If a cell ever errors on a fresh
   runtime, use **Runtime -> Restart and run all** once.

That is the whole flow. The cells below the first one are the same study written out
inline (the S-KBM envelope, the hybrid reward, the probe, and a short GRPO loop), so
you can read the mechanism step by step if you want.

## What you should see

Table 1, the reward-hacking probe (no GPU needed):

```
reward configuration                 infeasible mean   caught   feasible mean
preference-only  (w_hard=0)                    +10.0      0/5           +10.0
physics-grounded (w_hard=5)                   -490.5      5/5           +10.0
```

A preference-only reward cannot tell a physically infeasible completion from a
feasible one (0 of 5 caught); the unbounded physics term flips every infeasible
completion below every feasible one (5 of 5 caught).

Table 2, the small-scale GRPO run (hard-violation rate, before -> after training):

```
preference-only  (w_hard=0):  0.58 -> 1.00    (training hacks the reward)
physics-grounded (w_hard=5):  0.50 -> 0.00    (the floor drives violations to zero)
```

## What is in this package

- `moss_pigrpo_probe.ipynb`, the Colab notebook. Its first cell reproduces both tables;
  the rest walks through the method.
- `run_probe.py`, the model-free Table 1 reproduction (CPU, runs in under a second).
- `run_grpo_local.py`, the GRPO script behind Table 2 (Qwen2.5-0.5B-Instruct). It uses
  a GPU when one is present and falls back to CPU otherwise.
- `probe_results.json`, `grpo_results.json`, `grpo_results_phys.json`, the saved outputs.
- `COLAB_GUIDE.md`, a longer walkthrough with the free-tier path spelled out.

## Run it locally instead

```
pip install torch transformers accelerate
python run_probe.py                              # Table 1 (CPU, seconds)
STEPS=40 WHARDS=0.0,5.0 python run_grpo_local.py # Table 2 (uses a GPU if present)
```

`run_probe.py` writes `probe_results.json`; `run_grpo_local.py` writes a results JSON
and prints the base and trained hard-violation rates for each reward configuration.
