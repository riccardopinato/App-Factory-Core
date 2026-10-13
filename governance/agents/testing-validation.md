# Testing & Validation

Use the existing App Factory validation model. Do not invent a parallel certification ladder.

## Scope by risk and blast radius

Run the smallest set of checks that fully covers the changed behavior.

- Small mechanical/non-behavioral change: focused syntax/lint/build checks as applicable.
- Behavior change or localized bug fix: relevant tests plus regression coverage when appropriate.
- Cross-module, persistence, release, native, security, or contract change: expand validation to the affected integration surface.
- Release/certification work: follow FAST / FULL / CERTIFIED and the relevant Golden/AppLab/Release Reality rules.

"Test what you touch" means cover the real blast radius, not merely the edited file.

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
