# Phone Guard — Android alarm escalation donor evidence

Date: 2026-10-27

## Sources

Tabletop Motion Alarm:
- repository: `riccardopinato/Tabletop-Motion-Alarm`
- commit: `9e67bcbd84e8add7d183349644d3f6f6bbe9ffe0`
- relevant donor: siren, vibration, torch output, triggered alarm UI.

Phone Guard integration:
- repository: `riccardopinato/Phone-Guard`
- head: `aad8f9e44361380d554e9cebfa58810d2e1b3931`
- relevant files:
  - `alarm/FlashStrobeController.kt`
  - `alarm/AlarmVolumeController.kt`
  - `service/AlarmOutputController.kt`
  - `ui/screens/TriggeredAlarmScreen.kt`
  - alarm settings persistence/UI.

Luminous Circle:
- source supplied in the working chat as `luminous-circle (1).zip`;
- canonical repository/commit was not established during extraction;
- classification: **UNPINNED PATTERN INPUT**;
- no Luminous code/text is copied into App-Factory-Core.

## Reusable concepts

- output layer independent from detector;
- serial cancellable strobe;
- generation token preventing stale re-enable;
- guaranteed torch-off cleanup;
- configurable bounded flash rate;
- target STREAM_ALARM volume with prior-value restore;
- effective-volume diagnostic boundary;
- red pulsing warning screen;
- temporary per-window brightness and KEEP_SCREEN_ON restore.

## Important boundary

Android/OEM/DND policy can limit effective audibility and background Activity
launch. The Golden must not claim an unconditional system override.

At extraction time Phone Guard CI was still running and physical OEM validation
was pending.

No application code is copied into App-Factory-Core.
