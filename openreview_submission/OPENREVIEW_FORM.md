# OpenReview submission, field by field (MOSS @ COLM 2026)

Venue: Methods and Opportunities at Small Scale (MOSS), COLM 2026.
Submit at: https://openreview.net/group?id=colmweb.org/COLM/2026/Workshop/MOSS
Deadline: paper and notebook, June 30 2026 (AoE).
Track: Small-Scale Frontier (4-page main body). Not Free-Tier Colab (its PDF caps at 2 pages).

Paste the blocks below into the matching OpenReview fields. Field names vary slightly;
match by meaning. Anything not listed (consent checkboxes, conflicts) is standard.

## Title
Physics as a Hard Reward Floor: A Small-Scale, Controlled Study of Reward-Hacking Mitigation in RL Post-Training

## Authors
Enter your real name, email, and affiliation in the OpenReview author fields. OpenReview
keeps author identity hidden from reviewers under double-blind; the chairs still see it.
Do NOT put author identity in the PDF or the notebook (both are already anonymized).
Use your institutional email for the profile; a non-institutional profile can take up to
two weeks to moderate.

## Abstract
Reinforcement-learning post-training optimizes a reward that scores surface form, so a fluent but physically impossible completion can be rewarded by a rater yet is operationally wrong, a reward-hacking failure. We study a simple structural defense at small scale: an unbounded hard penalty on physical-law violations, added to the reward so that a single sustained violation dominates any preference signal, exposed to PPO, DPO, and GRPO through one shared reward path. A model-agnostic, CPU-only probe makes the effect exact: a preference-only reward never flags an infeasible completion (0/5 caught), while the unbounded physics term catches every one (5/5) without touching feasible completions. During a short GRPO run on a 0.5B model, the preference-only reward hacks the policy (hard-violation rate rises from 0.58 to 1.00) while the unbounded physics floor drives it to zero (0.50 to 0.00); everything reproduces in a released free-Colab notebook under 10^15 FLOPs.

## Keywords
reward hacking, RL post-training, GRPO, DPO, PPO, safety, small scale

## TL;DR (if the form has this field)
An unbounded hard penalty on physics violations gives the RL reward a floor that no preference signal can lift a violating completion above; a CPU-only probe (0/5 to 5/5 caught) and a 0.5B GRPO run (hard-violation rate 1.00 to 0.00) demonstrate it, all under 10^15 FLOPs in a free-Colab notebook.

## FLOP budget / compute statement (required for the Frontier track)
All experiments use under 10^15 FLOPs, far below the soft 10^20 MOSS cap. The reward-hacking probe is CPU-only and runs in seconds; the GRPO run uses one GPU (a free Colab T4 is enough) for a few minutes on Qwen2.5-0.5B-Instruct.

## Files to upload
1. Main PDF: paper.pdf (4 pages, anonymized).
2. Supplementary artifact ZIP: supplement.zip (the runnable notebook moss_pigrpo_probe.ipynb plus run_probe.py, run_grpo_local.py, the result JSONs, and the anonymized Colab guide). Reviewers run the notebook to check the main claims (FAQ Q4/Q6), so this is the reproducibility artifact.

## Double-blind checklist before you click submit
- PDF and notebook contain no name, affiliation, email, or GitHub URL (verified).
- Do NOT paste the public repo URL (github.com/arunshar/...) anywhere in the submission;
  the anonymized supplement.zip is the delivery. For a live anonymous link instead, use
  https://anonymous.4open.science pointed at the source repo.
- Author identity goes only in the OpenReview form fields, never in the files.
