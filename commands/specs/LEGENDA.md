# APP FACTORY — LEGENDA
Versione 1.0 | 2026-11-10 | ID: legenda | Effetto: SOLA LETTURA

## Source of truth
`commands/REGISTRY.json` is the canonical registry, and
`commands/LEGGENDA.md` is its deterministic generated view.
Use the current pinned Factory SHA. Never use a list remembered from chat.

## Execution contract
- `Legenda`: show the available commands, their effects and example syntax.
- `Legenda <filtro>`: filter the displayed list; do NOT execute the filtered
  command, or load the effects of unrelated commands.
- Show the registry counts dynamically, never use a hardcoded number in the
  operating contract.
- Missing or inconsistent registry/generated view => COMMAND LEGEND UNAVAILABLE.
- No repository mutations, workflow launches, secret or provider operations.

This file is a SHA-pinned command instruction, not an independent command
registry and not a reason to duplicate the authoritative metadata.
END COMMAND LEGENDA
