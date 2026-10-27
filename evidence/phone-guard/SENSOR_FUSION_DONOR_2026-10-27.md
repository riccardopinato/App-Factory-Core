# Phone Guard — Android sensor fusion donor evidence

Date: 2026-10-27

## Immutable donors

Pocket Guard / Pockara:
- repository: `riccardopinato/Pocket-Guard`
- commit: `b7b1c74de66e047c32083365b44561e42237b4fc`

Tabletop Motion Alarm:
- repository: `riccardopinato/Tabletop-Motion-Alarm`
- commit: `9e67bcbd84e8add7d183349644d3f6f6bbe9ffe0`

Integration pilot:
- repository: `riccardopinato/Phone-Guard`
- head: `aad8f9e44361380d554e9cebfa58810d2e1b3931`

## Donor files/patterns

Pocket:
- `SensorController.kt`
- `MotionDetector.kt`
- `RotationDetector.kt`
- `CalibrationCollector.kt`
- `SmartProtectionEngine.kt`
- `SensorCapabilities.kt`
- calibration/state/snapshot models
- SmartProtectionEngine and CalibrationCollector tests

Tabletop:
- calibrated motion baseline;
- MotionDetectionPolicy;
- same-boot/session recovery;
- Foreground Service reliability boundary.

## Generalized concepts

- accelerometer + gyroscope + proximity + light;
- capability gating;
- adaptive LOW_POWER/NORMAL/ALERT sampling;
- calibration separated from hot-path;
- hysteresis and time-window confirmation;
- bounded explainable confidence score;
- owner-check as policy outside raw sensor scoring;
- physical validation requirement.

## Evidence boundary

Phone Guard integration is a pilot and was not yet physically certified at the
time of extraction. This evidence supports a DRAFT / SPECIALIZED Golden only.

No donor code is copied into App-Factory-Core.
