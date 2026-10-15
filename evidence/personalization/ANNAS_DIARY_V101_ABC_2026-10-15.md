# Anna's Diary v1.01 A-C — Golden extraction evidence

Date: 2026-10-15
Repository: riccardopinato/Agenda-per-Anna
Merged main: def40d1fe3bbfc7f113948e72672a67e37edbc04

## Implemented
- v1.01-A: module preference contract, deterministic presets, legacy Complete,
  Cycle/Vault dependency normalization, JSON/backup behavior.
- v1.01-B: personalized first-run preset, commit on onboarding completion,
  Unified Capture reuse, existing-profile bypass, five-language copy.
- v1.01-C: module-aware Explore/Home/editor/Vault presentation, Personalize
  surface, no second state owner.

## Automated evidence
Tests inspected:
- test/v101a_module_preferences_test.dart
- test/v101b_personalized_onboarding_test.dart
- test/v101c_dynamic_personalization_test.dart

Merged-main workflows:
- Development checks #1156: PASS
- Deploy Anna's Diary Web #720: PASS
- Build lightweight ARM64 sideload APK #79: PASS

## Reusable invariant
VISIBILITY != OWNERSHIP != PERSISTENCE.
Hiding a module changes presentation only and does not delete user data.

## Boundary
v1.01-D Adaptive Home and v1.01-E final polish are not claimed here.
