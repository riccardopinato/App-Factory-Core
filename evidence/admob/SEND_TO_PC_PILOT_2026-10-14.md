# Send to PC — AdMob / UMP pilot evidence
Date: 2026-10-14

## Purpose

Register the first real Android-native App Factory donor for
`GOLDEN_ADMOB_SAFE_ADAPTIVE_MONETIZATION_v1_DRAFT.txt`.

This file records evidence boundaries only. It does not promote the Golden to
COPY-READY or CERTIFIED.

## Donor identity

- repository: `riccardopinato/Send-to-pc`
- stack: Kotlin / Jetpack Compose
- production donor: v1.27.6 / versionCode 43
- production commit: `f4f5b52ebf39b869782b3fb199a8d615662fb87d`
- Google Mobile Ads SDK Legacy: `25.5.0`
- Google UMP SDK: `4.0.0`

## Machine evidence

- Android release run: `38487703083` — SUCCESS
- AdMob production preflight run: `38487703176` — SUCCESS
- diagnostic ad-serving run: `38486941065` — SUCCESS
- exact production APK AppLab run: `38488312095` — SUCCESS
- production APK SHA-256:
  `5f36b5d4a1127a2a789bb0d3fb60394b3acf72a98c297987ee09878c69c4aaea`

Diagnostic lane used Google sample ad units and demonstrated:
- banner load success;
- interstitial load success;
- normal UMP lane;
- forced-EEA UMP diagnostic lane.

## Real defect discovered

The production code initialized Mobile Ads on `Dispatchers.IO` and then called
`InterstitialAd.load()` without switching back to the main UI thread.

Observed failure:

```text
IllegalStateException: #008 Must be called on the main UI thread
```

The global fail-safe then disabled the ads session, so the interstitial defect
also suppressed the banner path.

## Fix pattern validated

- keep `MobileAds.initialize()` on background thread;
- marshal interstitial load/show work to `Dispatchers.Main.immediate`;
- isolate interstitial preload/show failures to interstitial state;
- isolate banner load failures to banner state;
- do not disable the entire monetization session for a placement-local error.

## UMP production lesson

Before AdMob Privacy & messaging was configured, the runtime reported a publisher
misconfiguration indicating that no form was configured for the App ID.

After the European regulations message was configured/published and a public
privacy policy URL was set, the physical UMP flow worked.

Operational conclusion:

```text
UMP SDK integrated
!=
UMP message configured/published server-side
```

Publishing/editing the server-side message does not require a new APK if the
client UMP integration is already present.

## Physical evidence reported by project owner

Verified on a real Android device:
- app startup;
- production banner rendering;
- UMP / European regulations message rendering;
- consent choice flow;
- reopening privacy options / revocation path.

Not yet physically verified:
- production interstitial display at the intended natural break;
- complete no-fill/offline matrix;
- Premium/Remove Ads no-request path;
- Flutter/Web implementation.

## Promotion consequence

This donor materially strengthens the Android-native part of the Golden, but the
Golden remains:

```text
DRAFT / CANDIDATE — NON COPY-READY
```

The existing promotion gate still requires the missing Flutter/Web/Premium and
broader physical/failure evidence.
