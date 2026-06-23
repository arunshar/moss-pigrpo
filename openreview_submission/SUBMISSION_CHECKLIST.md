# MOSS @ COLM 2026: OpenReview submission packet

Everything in this folder is anonymized and ready to upload. Nothing here names
the author or links a personal repository.

## What to upload
- `paper.pdf` - the 4-page blind paper (main submission PDF).
- `supplement.zip` - the executable artifact: the Colab notebook, the two run
  scripts, the result JSONs, and the anonymized run guide. MOSS reviewers judge
  the claim by running the notebook (FAQ Q4/Q6), so this is what they execute.
- `abstract.txt` - title, keywords, and abstract as plain text to paste into the
  OpenReview form.

## Where to submit
OpenReview venue: https://openreview.net/group?id=colmweb.org/COLM/2026/Workshop/MOSS
Deadline: June 30, 2026 (AoE).

## Track
Submit to the **Small-Scale Frontier track**. That track allows a 4-page main body,
which is exactly what this paper is. The Free-Tier Colab track caps its optional PDF
write-up at 2 pages, so a 4-page paper does not fit there. The Frontier track wants
a measured small-scale result with a reported FLOP budget (0.5B GRPO, under 1e15
FLOPs vs the soft 1e20 cap), and it allows unlimited supplementary material plus an
optional artifact ZIP, which is where the notebook and code go. The free-Colab
notebook stays as the reproducibility artifact that reviewers run.

## Compute statement (for the form, if asked)
All experiments use under 1e15 FLOPs, far below the 1e20 MOSS cap. The probe is
CPU-only; the GRPO run uses one GPU (a free Colab T4 is enough) for a few minutes.

## Step by step
1. Sign in to OpenReview and open the MOSS venue, then "New Submission".
2. Title and Abstract: copy from `abstract.txt`. Keywords: the line in that file.
3. Authors: enter the real author identity in the OpenReview form fields. This is
   correct for double blind: OpenReview hides author metadata from reviewers while
   the program chairs can see it. Do NOT put author identity in the PDF or notebook.
4. Upload `paper.pdf` as the submission PDF.
5. Upload `supplement.zip` as supplementary material.
6. Select the track (above) and answer the compute / reproducibility questions.
7. Submit, then confirm the PDF renders and the supplement downloads.

## Double-blind do / do not
- DO keep the PDF and notebook free of name, affiliation, email, and any GitHub URL.
- DO enter author identity only in the OpenReview form (not in the files).
- DO NOT link the public mirror repo. Its URL still contains the author's account
  name, so linking it would deanonymize the submission. The supplement zip is the
  anonymous delivery path. For a live anonymous link instead of a zip, use
  https://anonymous.4open.science pointed at the source repo and paste that link.

## Pre-submit verification (re-run any time)
From the repository root:
- `python3 scripts/anonymize.py --check build/anon` -> "anonymization check OK".
- `pdfinfo openreview_submission/paper.pdf` -> Author is "Anonymous Authors".
- `unzip -l openreview_submission/supplement.zip` -> notebook + scripts present.
