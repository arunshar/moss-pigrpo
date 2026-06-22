# Anonymized mirror: how it works and how to finish the setup

This repo (`arunshar/moss-pigrpo`) is the real, named source. A GitHub Action keeps
an anonymized copy in sync at `arunshar/moss-pigrpo-anon` for double-blind review.

## How the sync works
On every push to `main`, `.github/workflows/anonymize-mirror.yml`:
1. Runs `python3 scripts/anonymize.py --src . --out build/anon` to build a scrubbed
   tree (strips the GitHub handle and author name, rewrites the notebook's one-click
   cell to run from uploaded files with no clone URL, drops any Colab "Open in Colab"
   badge, clears notebook outputs, and writes a clean Colab guide).
2. Runs `python3 scripts/anonymize.py --check build/anon`, which fails the job if any
   author identifier survived.
3. Force-pushes the scrubbed tree to `arunshar/moss-pigrpo-anon` as a single
   `Anonymous <anon@example.com>` commit, so the mirror never carries real-name history.

The scrubber is robust to Colab "Save a copy to GitHub" rewrites; it never depends on
a specific cell being present.

## One-time step to enable the automatic push
The job runs on every push, but the push to the mirror is skipped until a repository
secret named `MIRROR_PAT` exists. Without it, the mirror only updates when reseeded by
hand. Add the secret once to turn on real auto-sync.

### Part 1: create a least-privilege token
1. Go to https://github.com/settings/tokens?type=beta
   (avatar -> Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens).
2. Click **Generate new token**.
3. Token name: `moss-mirror-push`. Expiration: 90 days (or your choice).
4. Resource owner: **arunshar**.
5. Repository access -> **Only select repositories** -> pick **`arunshar/moss-pigrpo-anon`**
   (the repo the workflow pushes to).
6. Permissions -> Repository permissions -> **Contents -> Read and write**. Leave the rest at No access.
7. Click **Generate token** and copy the `github_pat_...` value (shown only once).

### Part 2: add it as a secret on this source repo
1. Go to https://github.com/arunshar/moss-pigrpo/settings/secrets/actions
2. Click **New repository secret**.
3. Name: `MIRROR_PAT` (exactly). Value: paste the token. Click **Add secret**.

### Part 3: verify
1. Actions tab -> **anonymize-mirror** -> **Run workflow** -> Run (on `main`).
2. Open the run. The **Push to anonymized mirror** step should print
   `Mirrored to arunshar/moss-pigrpo-anon.` instead of the "secret not set; skipping" line.
3. Confirm the mirror repo's latest commit timestamp just updated.

Note: the `MIRROR_PAT` used for the portfolio mirror is a secret on a different repo and
is not shared, so you still add one here. If that token is a classic token with `repo`
scope, the same value works; just add it under the name `MIRROR_PAT` on this repo.

## Editing the notebook in Colab safely
- The mirror is self-healing, so a Colab save will not break it. But to avoid re-adding
  the badge: in Colab use **File -> Save a copy in GitHub** and **uncheck
  "Include a link to Colaboratory"** before saving.
- Keep the first one-click cell if you want it in the source repo; the mirror re-injects
  a clean, no-clone copy regardless.

## Manual reseed (if you ever need it before the secret is set)
```
python3 scripts/anonymize.py --src . --out build/anon
python3 scripts/anonymize.py --check build/anon
cd build/anon
git init -b main
git -c user.name=Anonymous -c user.email=anon@example.com add -A
git -c user.name=Anonymous -c user.email=anon@example.com commit -m "Anonymized snapshot for MOSS @ COLM 2026 double-blind review"
git remote add origin https://github.com/arunshar/moss-pigrpo-anon.git
git push --force origin main
```

## Double-blind reminder
Do not link the mirror repo URL in the OpenReview submission; the owning account name is
visible. Upload `openreview_submission/supplement.zip`, or use anonymous.4open.science for
a live anonymous link. See `openreview_submission/SUBMISSION_CHECKLIST.md`.
