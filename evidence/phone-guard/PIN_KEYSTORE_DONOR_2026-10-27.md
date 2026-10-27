# Phone Guard — local PIN / Android Keystore donor evidence

Date: 2026-10-27

## Immutable donors

Tabletop Motion Alarm:
- `riccardopinato/Tabletop-Motion-Alarm@9e67bcbd84e8add7d183349644d3f6f6bbe9ffe0`
- PBKDF2WithHmacSHA256;
- random salt;
- 210,000 iterations;
- MessageDigest.isEqual.

Pocket Guard / Pockara:
- `riccardopinato/Pocket-Guard@b7b1c74de66e047c32083365b44561e42237b4fc`
- PBKDF2 verifier;
- HMAC-SHA256 keyed by AndroidKeyStore SecretKey;
- constant-time verification pattern.

Phone Guard:
- integration head `aad8f9e44361380d554e9cebfa58810d2e1b3931`;
- combines 210,000-iteration PBKDF2 with AndroidKeyStore HMAC hardening.

## Generalized boundary

This is a local PIN verifier pattern, not encrypted payload storage and not a
password manager.

Restore/reinstall/Keystore invalidation behavior remains a required fail-closed
test area before promotion.

No donor code is copied into App-Factory-Core.
