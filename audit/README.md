# Audit — App Factory Core

Questa cartella è il catalogo canonico del comando **Audit**.

## Uso

- **`Audit`**: audit 360° dell'app/progetto attualmente riconoscibile nella chat.
- **`Audit Notes-Ecosistema`**, **`Audit Anna's Diary`**: target esplicito.
- **`Audit tutte le app`**: audit trasversale con inventario dei repository.
- Se nessuna app è identificabile, chiedere il nome dell'app.

## Sorgente canonica

[MASTER_AUDIT_360_APP_FACTORY_v1.txt](MASTER_AUDIT_360_APP_FACTORY_v1.txt) contiene il prompt integrale v1.0 (7 novembre 2026). Non duplicarlo nel Master Core.

Il bootstrap risolve una sola volta `CURRENT.yaml` + Master + Index/Registry e seleziona il route `audit` esistente in `MODULE_MAP.json`. Poi carica questo prompt; Product Bible, roadmap e regole di accesso delle singole app prevalgono sullo scope, mentre Master/Golden prevalgono sulle regole operative. Modalità **READ_ONLY**: nessun cambiamento a codebase, roadmap, issue, cloud, merge, deploy o store.

`audit/` è la libreria di istruzioni; `audits/` raccoglie report storici/evidence. Non alterare i moduli legacy byte-exact della Factory v26.8 per registrare questo comando.

## Registro delle attività aperte per audit ricorrenti

[UNSLOP_UI_AZIONI_APERTE_2026-11-19.md](UNSLOP_UI_AZIONI_APERTE_2026-11-19.md) conserva i gate di accettazione ancora aperti del pilota Unslop UI/Anti-AI 64. In un audit Factory trasversale, o dei consumer coinvolti, verificare e riportare lo stato corrente degli ID UNSLOP-FT-01…04 senza confondere snapshot storici e HEAD GitHub. Consultarlo in **sola lettura** durante il comando `Audit`; la chiusura degli item richiede un'azione di manutenzione autorizzata, non è un effetto dell'audit.

## ChatGPT Project

Il comando breve funziona quando la chat appartiene a un Project con istruzioni che fanno risolvere App-Factory-Core/CURRENT.yaml, come il pointer `bootstrap/PROJECT_CUSTOM_INSTRUCTION.txt`. Una modifica GitHub non aggiorna automaticamente le impostazioni dei Project; fuori da tale contesto occorre impostare il pointer.

## Modifiche future

Versionare gli aggiornamenti del prompt, mantenere coerenti Core, mirror e fallback generato, validare sul commit finale. Il comando di solo audit non conferisce autorizzazione a implementare.
