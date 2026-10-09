# Security

Do not commit signing keystores, passwords, API secrets, service-account private
keys, OAuth client secrets or production credentials.

Golden documents may contain secret variable names/placeholders, never values.

If a credential is committed, treat it as compromised: revoke/rotate first,
then remove it from repository/history as appropriate.
