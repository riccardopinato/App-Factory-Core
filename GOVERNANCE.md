# App Factory Core Governance

## Canonical update flow

CURRENT baseline -> branch -> coherent change -> PR -> Factory validation GREEN
-> review -> merge -> new main SHA becomes the next Factory baseline.

Direct writes to `main` are reserved for documented recovery/emergency work.

## Required main protection

The repository should enforce a ruleset/branch protection for `main`:
- require pull request before merge;
- require **Validate App Factory Core / validate**;
- block force pushes;
- block branch deletion;
- owner/admin emergency bypass only when necessary.

A workflow file does not itself protect `main`.

## Versioning and freshness

Migration into the Core is not review evidence.
`migrated_at`, `last_content_reviewed_at` and
`last_provider_verified_at` are distinct facts.
Provider-sensitive entries without current provider evidence are NEEDS_REVIEW.

## Agent governance

- Root `AGENTS.md` is the canonical repository-local operating contract for agents modifying App-Factory-Core.
- It does not replace CURRENT.yaml, the Master Prompt, Golden Rules, Product Bible, Roadmap, or executable implementation truth.
- Detailed agent policies live under `governance/agents/` and should be loaded only when relevant.
- Tool-specific instruction files must be thin pointers/imports or deterministic generated bridges from the canonical contract; they must not become independent policy sources.
- Changes to AGENTS.md or its governance modules follow the same branch -> validation -> PR -> review flow as other Core governance changes.
- Agents must not self-modify central governance as an unreviewed reaction to a single session correction.

## v27 synchronized modular/full policy update (candidate)

When a user requests an update to the Master Prompt or App-Factory-Core, update both the canonical modular v27 rule sources and the generated *operative* full v27 fallback in the same branch/PR. `scripts/build_v27_fallback.py --write` produces the fallback and updates the manifest source/fallback pins; CI runs `--check` and resolver tests to reject drift. Never hand-edit the fallback. The original v26.8 full Master remains an immutable historical recovery asset, not the current-policy fallback. Until v27 activation, the version resolved by CURRENT.yaml remains independently authoritative and must be updated if the requested policy change affects currently active rules. No silent fallback to stale policy, no branch-protection bypass.
