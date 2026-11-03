# Golden v28 reference harness extensions
Date: 2026-11-03
Source baseline before this update: App-Factory-Core@9adf94ed73e17b88806bbf4ef1d0d976ba244ff4
Master v27 / Index v28 / Registry v2 unchanged (59 entries).

1. Spatial: reference_engines/lib/src/spatial_clustering.dart now exposes
   deterministic transitive radius and zoom-grid clustering. Core PR #52
   merged be73f82f3006687340b6078e18035722b0e968c4.
   Exact-main CI Dart PASS https://github.com/riccardopinato/App-Factory-Core/actions/runs/41612802131 .
   No consumer or physical map/FPS evidence.

2. Performance: reference_engines/lib/src/performance_fixtures.dart seeded
   generator + deterministic digest + warmup/repetitions + p50/p95 with explicit
   source SHA and runner identity. Same PR/CI as above.
   Not a complete cross-app regression platform: no independent consumer,
   runner comparability or performance threshold proven.

3. Canvas: reference_engines/lib/src/canvas_ink.dart pure Dart camera,
   anchor zoom/pan, scene codec, bounded strokes/nodes and undo/redo.
   Core PR #53 merged 9adf94ed73e17b88806bbf4ef1d0d976ba244ff4,
   exact-head Dart CI PASS
   https://github.com/riccardopinato/App-Factory-Core/actions/runs/41613296577 .
   Partial extraction only: lasso, widget, gestures/stylus, full Notes interop
   and physical 20k/50k FPS tests not included.

All three remain DRAFT. Technical source availability is not E5 consumer
reuse and never equates to Android or release certification.
