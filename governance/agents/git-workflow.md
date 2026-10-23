# Git & Pull Request Workflow

This module complements GOVERNANCE.md and the Master Prompt.

## App-Factory-Core changes

Normal flow:

Factory baseline
-> task branch
-> coherent change
-> local/CI Factory validation
-> pull request
-> review / required repository gates
-> merge when the authorized scope and merge gates are satisfied
-> new main SHA becomes the next Factory baseline

Do not push ordinary Factory governance changes directly to main.

## Before mutation

Check:
- intended repository;
- branch/ref;
- baseline SHA;
- whether the base moved when that matters;
- existing dirty/untracked work when using a local checkout;
- whether another writer owns the same branch/workspace/file set.

Do not overwrite user-owned changes.

## Branch and workspace discipline

Keep main stable.

Prefer one writer per branch/workspace. Concurrent writers need isolated workspaces and non-overlapping ownership.

Do not force-push main or a shared branch.
Do not rewrite shared history merely to make a PR cleaner.

## Coherent Factory commits

When a framework version changes, keep the required coupled artifacts coherent in the same commit as defined by the Master/README, including as applicable:

- versioned Master;
- CURRENT Master alias;
- CURRENT.yaml;
- versioned Golden Index;
- CURRENT Golden Index alias;
- Golden Registry;
- relevant Golden documents;
- validator/schema changes;
- CHANGELOG.

A partially updated resolver state is invalid.

## Pull requests

Use the repository PR template when present.

A Factory PR should state:
- baseline SHA;
- outcome;
- affected governance surfaces;
- provenance for external patterns;
- validation performed;
- known limitations or deferred work.

Once implementation is authorized, no separate user approval is required for a PR merge.

Merge only when the PR remains inside the authorized scope, required checks on the exact head are green, the PR is mergeable, and no blocking review, credential, user-action gate, unresolved product decision, or separately authorized irreversible action remains. If the user asks to stop before merge or review first, do not merge.

Audit/read-only work does not imply merge authorization. Repository branch protection or a platform-required human approval remains binding.

CI GREEN proves repository consistency only within the validator's contract. It does not certify downstream app runtime behavior.
