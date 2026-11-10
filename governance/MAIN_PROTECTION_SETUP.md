# Main protection — required GitHub repository setting

As of 2026-11-10, GitHub REST showed `branches/main.protected=false` and
`rulesets=[]`; the connected GitHub integration could READ these settings but
did not expose a write action for rulesets/branch protection.

**This is a required USER/ADMIN ACTION, not something a repository commit can
activate.** A green workflow alone does NOT prevent an invalid direct push.

1. Open [GitHub Rules](https://github.com/riccardopinato/App-Factory-Core/settings/rules).
2. New ruleset → New branch ruleset; target `main`, enforcement **Active**.
3. Require pull request before merging, require status checks from
   `Validate App Factory Core` / job `validate`, block force pushes and
   deletion, and retain an owner emergency bypass only where strictly necessary.
4. Confirm status-check naming in the GitHub UI before selecting the required
   check. Do not require an unrelated/obsolete job name.
5. Test an ordinary PR and verify that a failing required check blocks merge.
   If the plan does not support repository rulesets, inspect classic branch
   protection as an alternative. Never assume it was activated automatically.
6. Verify after setup using authenticated GET:
   `/repos/riccardopinato/App-Factory-Core/branches/main` should report
   `protected: true`; inspect `/rulesets` or branch protection for exact
   enforcement. A configuration screenshot is weaker than actual API state.

Until the UI setting is confirmed: `MAIN_PROTECTION = BLOCKED_USER_ACTION`.
Do not bypass this by claiming that a CI PASS equals a protected branch.
