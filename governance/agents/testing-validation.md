# Testing & Validation

Use the existing App Factory validation model. Do not invent a parallel certification ladder.

## Scope by risk and blast radius

Run the smallest set of checks that fully covers the changed behavior.

- Small mechanical/non-behavioral change: focused syntax/lint/build checks as applicable.
- Behavior change or localized bug fix: relevant tests plus regression coverage when appropriate.
- Cross-module, persistence, release, native, security, or contract change: expand validation to the affected integration surface.
- Release/certification work: follow FAST / FULL / CERTIFIED and the relevant Golden/AppLab/Release Reality rules.

"Test what you touch" means cover the real blast radius, not merely the edited file.

## Adaptive execution: fast preflight, unchanged gates

Master v26.8 section 1.3 is a **routing policy**, not an extra QA tier.
Choose a minimal targeted preflight before expensive suites; run mandatory
repository checks and risk-appropriate validations afterwards on the integrated
exact head. Typical cheap preflights: source compilation/typecheck, resource
consistency, migration schema checks, or test-APK compilation when instrumented
tests changed. Do not install a new tool merely to satisfy these examples.

Avoid rerunning full CI with a known local compile failure. Reuse a green run
or built artifact only when the source SHA, build contract, toolchain, signing
identity, artifact hash and repository-required freshness semantics match.
A changed source commit invalidates an older exact-head CI result. This also
applies to parallel workstreams: independently green branches do not validate
the merged tree.

For policy smoke review, exercise the scenarios in Master section 1.3:
localized copy fix (DIRECT), separate modules (PARALLEL), data migration
(CONTROLLED), audit-only request (READ-ONLY), and new commit following green CI
(OLD HEAD NOT GREEN). These are expected decisions, not proof of model behavior.

## Required semantics

- Behavior change should have executable coverage when practical.
- A bug fix should have a regression test when it can be expressed reliably.
- Build green != feature verified.
- Web Preview != native certification.
- Permission granted != capability healthy.
- Artifact built != artifact distributed or physically verified.
- Do not convert BLOCKED or NOT VERIFIED into PASS.

## Cleanup ordering

When implementation includes obsolete-code, dependency, or asset cleanup:

1. make the behavior change;
2. perform the bounded cleanup;
3. run the relevant final validation on the cleaned tree.

Tests run before deletion are useful diagnostics but are not final-state evidence.

## Evidence discipline

Never claim a command, test, build, runtime journey, AppLab run, physical-device check, or release step happened unless evidence exists.

Report:
- checks executed;
- their result;
- relevant scope;
- checks not executed and why;
- failures/blockers;
- physical validation still required.

For native/runtime-sensitive claims, prefer real runtime evidence over inferred capability.

## Instruction and process validation

When a governance instruction contains deterministic commands, file invariants, generated bridges, or other machine-checkable behavior, add deterministic tests/validator checks where practical.

For high-risk agent instructions, consider an evaluation that tests whether an agent can follow the instruction, with:
- a positive control;
- a negative control;
- a regression case for a previously observed failure.

Do not treat keyword presence alone as proof that an instruction is behaviorally effective.
