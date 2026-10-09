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
