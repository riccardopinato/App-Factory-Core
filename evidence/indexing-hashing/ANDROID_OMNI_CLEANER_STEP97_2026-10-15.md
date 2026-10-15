# Android Omni Cleaner Step 9.7 — physical performance evidence

Date: 2026-10-15
Repository: riccardopinato/Android-Omni-Cleaner
Current main observed: 130b249a0f2c572951fba896a5e2d69800009855
Current Android CI #387: PASS

Exact Step 9.7 physical APK source:
436e884886dbc7e034547b3a7b7299a9cd649f7b

Device: Xiaomi M2101K6G / Android SDK 33 / 8 processors.
Real library: 87,136 files.

Measured:
- cold inventory 61,064 ms;
- scanner-only cold 43,167 ms;
- warm persistent HIT 2,599 ms;
- warm speedup 23.50x;
- warm file-count delta 0;
- hot memory HIT 1 ms;
- SHA-256 sample 128 MiB across 5 files;
- 1 worker 573.99 MiB/s;
- 2 workers 920.86 MiB/s;
- 4 workers 1,267.33 MiB/s;
- peak in-flight 1/2/4;
- thermal 0 -> 0;
- battery temperature 35.3 -> 37.2 C;
- observed heap high-water 82,121,544 bytes.

The first real run exposed two regressions: RAM TTL inherited stale persisted
timestamp and warm reuse re-statted every indexed file. Both were corrected.
Schema v2 adds directory fingerprints; destructive paths still revalidate live
source.

Promotion boundary:
second representative lower-end/older device remains pending.
