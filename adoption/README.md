# Factory Adoption Kit v1

Purpose: activate the central App Factory working mode in a new or existing app
without copying the Factory rules into the app repository.

The app keeps only `APP_FACTORY_ADOPTION.yaml`. The canonical profile remains
in App-Factory-Core and is resolved through `CURRENT.yaml`.

## Standard flow

Dry run:

```bash
python scripts/adopt_factory_mode.py \
  --repo-root /path/to/app \
  --repository owner/repository \
  --json
```

Apply:

```bash
python scripts/adopt_factory_mode.py \
  --repo-root /path/to/app \
  --repository owner/repository \
  --apply
```

Validate:

```bash
python scripts/validate_factory_adoption.py --repo-root /path/to/app
```

## Workflow fallback rule

Existing workflows are inspected and preserved.

The adopter NEVER edits, deletes or replaces files under `.github/workflows`.
If workflows already exist, the result is `PRESERVE_EXISTING_AND_INTEGRATE`.
The ADOPT_FACTORY_MODE playbook may then add only a bounded integration delta,
or a separate Factory workflow when no equivalent capability exists.

INTEGRATE BEFORE REPLACE.
CUSTOM WORKFLOW != OBSOLETE WORKFLOW.

Any later workflow edit follows normal repository governance, tests, exact-head
validation and bounded code-hygiene rules.
