# Code Hygiene — Bounded Cleanup

Apply this module to substantial implementation, bug fixes, refactors, feature removals, migrations, configuration changes, and dependency changes.

## Core invariant

Adding a replacement without evaluating removal of the superseded implementation is incomplete work.

Prefer deletion and consolidation when behavior is safely superseded. Do not preserve code only "just in case".

## Mandatory affected-scope sweep

Inspect the changed subsystem for:

- dead or unreachable code;
- superseded implementations;
- duplicate repositories, services, coordinators, schedulers, listeners, workers, state owners, or feature paths;
- unused functions, classes, variables, imports, routes, configuration, and resources;
- stale temporary workarounds;
- obsolete compatibility layers;
- stale feature flags;
- stale TODOs that describe already-resolved work;
- commented-out implementations;
- deprecated APIs touched by the task;
- unused dependencies;
- unused assets and translations;
- orphan media/files/cache created by removed behavior;
- reminders, jobs, alarms, subscriptions, callbacks, or background work orphaned by deletion.

## Bounded-cleanup rule

Cleanup is mandatory when the task clearly makes code obsolete, but it stays inside the affected dependency and behavior neighborhood.

Do not:
- launch unrelated architectural rewrites;
- rename or reformat unrelated modules;
- upgrade unrelated dependencies;
- delete historical migrations, compatibility contracts, generated files, vendored code, or release evidence merely because they look old;
- remove behavior whose callers or persistence implications have not been checked.

When a broader cleanup opportunity is real but outside scope, report it separately instead of hiding it in the current diff.

## Before deletion

Verify as applicable:

1. references/callers;
2. runtime registration or reflection;
3. persistence/migration role;
4. platform manifests/configuration;
5. tests and fixtures;
6. localization/resources/assets;
7. background scheduling and lifecycle hooks;
8. public/API compatibility;
9. import/export or backup compatibility.

Unknown impact is not evidence that deletion is safe.

## Dependencies and assets

Before adding a dependency, apply the Master Dependency Admission Rule.

When a feature is removed or replaced:
- identify packages no longer required;
- remove them when no remaining code depends on them;
- update lock/config files coherently;
- remove assets only after reference checks;
- check app-size and platform implications when material.

Do not add a package for trivial stable logic already provided by the language/framework/project.

## Bug fixes

Prefer root-cause fixes over symptom suppression.

For a bug fix:
- inspect nearby code for the same failure pattern;
- add a regression test when appropriate;
- remove the workaround or broken parallel path when the proper fix supersedes it.

A bug fix that leaves both the broken and replacement paths active requires an explicit reason.

## Final-state validation

Cleanup changes the final artifact. Therefore rerun relevant validation after cleanup:

- formatter/linter/analyzer;
- focused tests;
- broader tests according to blast radius;
- build when applicable;
- runtime/physical validation when required by the capability.

A green check obtained only before cleanup does not validate the final tree.

## Evidence

For substantial work, the completion report should state:
- what obsolete/superseded code was found;
- what was removed or deliberately retained;
- dependency/asset changes;
- final checks run after cleanup;
- any cleanup finding intentionally left outside scope.
