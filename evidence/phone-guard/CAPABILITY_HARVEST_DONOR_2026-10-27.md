# Phone Guard — Capability Harvest / assembly donor evidence

Date: 2026-10-27

## Sources

- target repository: `riccardopinato/Phone-Guard`
- target integration head: `aad8f9e44361380d554e9cebfa58810d2e1b3931`
- Tabletop donor: `riccardopinato/Tabletop-Motion-Alarm@9e67bcbd84e8add7d183349644d3f6f6bbe9ffe0`
- Pocket donor: `riccardopinato/Pocket-Guard@b7b1c74de66e047c32083365b44561e42237b4fc`
- Phone Guard PR: #1, draft at extraction time

## Reusable process observed

The pilot evaluated components/capabilities rather than selecting one whole app
as the only base.

Canonical decisions used:
- PRESERVE;
- IMPORT;
- REBUILD;
- DROP.

Observed examples:
- Tabletop foreground-service lifecycle/recovery: PRESERVE;
- Tabletop alarm output/history: PRESERVE;
- Pocket sensor fusion/calibration/Journey concepts: IMPORT;
- unified settings/service contracts: REBUILD;
- duplicate Pocket alarm/history implementations: DROP after comparison.

## Product/repository boundary

Phone Guard is intentionally a separate repository because Tabletop and Pockara
remain separate products.

The pilot therefore copies/adapts internal donor code into a new product-owned
namespace instead of introducing runtime coupling to donor repositories.

## Evidence boundary

At extraction time:
- donor refs are immutable;
- target PR exists;
- Phone Guard CI was running, not yet final;
- no physical-device certification is claimed.

No application source code is copied into App-Factory-Core by this record.
