# World Days lifetime Remove Ads — Golden extraction evidence

Date: 2026-10-15
Repository: riccardopinato/World-Days
Merged main: b44ceeafa95e6add4d561ab658377ab25ecf7cc4

## Implemented
- provider-agnostic EntitlementService;
- BillingAdapter abstraction;
- Flutter in_app_purchase mobile adapter;
- Web/unsupported stub;
- one-time lifetime Remove Ads;
- purchase stream;
- pending/cancel/error no-grant;
- exact product + verification payload mapping;
- persisted entitlement before provider completion;
- offline cached lifetime;
- user-initiated restore;
- ProductLimits / ads-suppression boundary.

## Tests
test/core/entitlement_service_test.dart covers free, offline lifetime, pending/
cancel, verified purchase, async update, restore and no-ad-request invariant.

## CI
- Development checks #127: PASS
- Deploy Web Preview #21: PASS

## Provider boundary
docs/BILLING_SETUP.md states:
- in_app_purchase 3.3.1;
- provider adapter implemented;
- Play catalog/sandbox evidence still required;
- client store-state acceptance is not server-side receipt verification.

Conclusion:
generic Entitlement Contract has real provider-decoupled donor evidence;
Play Billing provider Golden remains DRAFT.
