# Capability — comando operativo App Factory
Versione: 1.0 — 07/11/2026

**Scrivi `Capability`** in una chat che usa il pointer App-Factory-Core: avvia una **riconciliazione incrementale dell'intero portafoglio**, con aggiornamento canonico delle capability per ogni app e rigenerazione delle priorità.

Altri comandi: `Capability Notes-Ecosistema`, `Capability Anna's Diary`, `Capability tutte le app`, `Capability priorità`.

**Contratto completo:** [MASTER_CAPABILITY_SYNC_v1.txt](MASTER_CAPABILITY_SYNC_v1.txt).

## Due repository, una sola source of truth per dato
- App-Factory-Core (questa cartella) è l'**owner delle regole e del comando**.
- [Idee-app-Archivi-riferimenti/12-CAPABILITY-E-IMPLEMENTAZIONI](https://github.com/riccardopinato/Idee-app-Archivi-riferimenti/tree/main/12-CAPABILITY-E-IMPLEMENTAZIONI) è l'**owner del registro dati**: `REGISTRO_CAPABILITY.json`, `SOURCE_INVENTORY.json`, generatori e viste per app.
- I singoli repo app sono l'**owner delle evidenze del codice**, CI, release e delle scelte di prodotto (Product Bible, roadmap).

Non creare copie di tutti i CAP in Core: gli status per-app cambiano frequentemente e richiedono un unico database versionato.

## Stato e decisione
Il campo tecnico `app_states` misura livello di evidenza (PROPOSTA → SOURCE_CONFIRMED → CI_VERIFIED → DEVICE_VERIFIED → RELEASE), non la decisione prodotto. `SCARTATA`, `RINVIATA`, `APPROVATA`, `IN_ROADMAP`, `FUORI_SCOPE` vanno registrate separatamente per app e solo con decision evidence; il contratto descrive l'estensione compatibile se ancora assente.

## Scritture ammesse
Solo modifiche evidence-based al catalogo, con branch/PR, generatori, check, merge autorizzato. Nessuna modifica ai repository app, a Golden, a roadmap o a codebase su un semplice `Capability`. Se non si riesce a completare la rigenerazione/CI, dichiarare BLOCKED e non un aggiornamento concluso.

## Aggiornamento incrementale
Verifica i commit SHA; rianalizza repository e capability solo quando cambiano sorgente, evidenza o decisioni, o se la copertura precedente è incompleta. Un controllo senza delta produce NO-OP. Le idee scartate restano nello storico ma escono dalla coda operativa della singola app.

Non è un webhook: il comando esegue il lavoro **nella conversazione corrente**. Eventuali controlli periodici esistenti restano workflow separati. Gli agenti possono usare GitHub solo quando il relativo accesso è realmente disponibile.
