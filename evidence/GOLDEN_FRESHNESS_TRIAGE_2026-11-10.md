# Golden provider/freshness review queue — 2026-11-10

Factory baseline: v27 ACTIVE; Golden Index v29; Registry v2.
Source: `golden/GOLDEN_REGISTRY.yaml` at PR #93.
This is triage, **not** a provider re-verification. No item below is newly
certified, copy-ready or production/consumer verified by this report.

## First priority: widely reusable COPY_READY but NEEDS_REVIEW

| ID | Domain | Admission | Provider check |
|---|---|---|---|
| `google_auth_supabase` | Google OAuth / Supabase | COPY_READY | Missing |
| `secure_storage_android_keystore` | Android protected storage | COPY_READY | Missing |
| `notification_reliability` | Notifications / provider and OS | COPY_READY | Missing |
| `localization` | Flutter/localization | COPY_READY | Missing |
| `theme_m3` | Material 3/platform theming | COPY_READY | Missing |

These may still be copied with an explicit review and consumer tests; freshness
CURRENT and COPY_READY are different dimensions. Validate provider docs, SDK
versions, policy and permissions **at adoption time**, and record exact links,
date, test surface and any mismatch.

## Second priority: CANDIDATE, not auto-admissible

| ID | Category |
|---|---|
| `android_signing_release_identity` | release |
| `play_billing_lifetime_entitlement` | monetization |
| `android_native_reliability` | native |
| `android_alarm_escalation` | native |
| `android_local_pin_verifier_keystore` | security |
| `sensor_fusion_android` | native |
| `capability_permission_health` | native |
| `fastlane_android_delivery` | release |
| `app_icon_branding` | UI |
| `coderabbit_pr_review` | governance |
| `oss_reuse_reconnaissance` | governance |

Until independently verified, retain CANDIDATE and NEEDS_REVIEW. Provider
sensitive items must not be promoted from changed document timestamps alone.

## Acceptance for each review

1. Fresh official provider policy/documentation link and date verified.
2. Pinned package/API versions and license/commercial-use boundary checked.
3. Adapter/source tests and consumer compatibility scope recorded.
4. Hardware/auth/billing/notification delivery cases validated on the
   relevant actual surface (device/provider/store) or marked NOT_VERIFIED.
5. Golden Registry freshness/provenance updated with its Index/status only
   on actual evidence; all Golden promotions require their separate gates.

## Do not infer

A green Core validator tests registry/document consistency, NOT OAuth,
Play Billing, hardware sensor, notification receipt or keystore behavior.
