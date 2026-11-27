# OpenSpec-derived incremental change reconciliation — governance

Implementation status: SOURCE CANDIDATE. No certification, agent execution, new scheduler, or default rollout.

1. Ownership: Product Bible/roadmap approve behavior; Master v27 and Golden govern; AppLab/GitHub prove source/CI; device/provider approvals remain separate. This adapter cannot grant approvals.
2. Contract: optional per-requirement ADDED/MODIFIED/REMOVED/RENAMED delta including prior spec, FR and exact source SHA. Preserve v1 manifest compatibility. Exclusions remain scope.excludes. FAST remains compact; removal cannot be FAST.
3. Before editing: read app Product Bible, roadmap, AGENTS, current source HEAD, existing PRs, and relevant canonical requirements. Convert findings to bounded proposed deltas, no product change without authorization.
4. Drift: run read-only checker with externally collected repo HEAD, complete open-PR inventory and canonical snapshots. A missing inventory is BLOCKED. Overlap in PR requirements is BLOCKED. Path overlap needs human review. Checker does not query GitHub, authenticate snapshots or certify absence of other changes.
5. After integration: require merged PR, independently observed merge SHA, postmerge exact-SHA CI, individual required check receipts, trusted product approval and controlled human/device/provider gates where applicable. Closeout script only previews changes; trusted operator reviews and publishes canonical edits by normal PR/exact-head checks. Never auto-mutate Product Bible.
6. Archive: preserve previous requirement identity and source SHA, distinguish proposed/implemented/source CI/device/production, retain audit trail and rollback reference. If trust receipts or old snapshot are incomplete, HOLD only the affected change.
7. AppLab and Agent Core remain their respective authorities. A manifest and source-only test cannot claim physical install, real Windows execution, token savings, signed APK, store release or autonomous success.
8. Comparative pilots: one bounded FAST/direct change and one STANDARD dependency change, with before/after elapsed and token measurements only when instrumented. Avoid false estimates.

Source concept: Fission-AI/OpenSpec, MIT, version 2.2.0, upstream source f1cd852f4edce22b8df9548a4df889172ca8ff25. Adapted approach; no CLI installed.
