# Legenda — registro pubblico dei comandi App Factory

Scrivendo **`Legenda`** in una chat collegata al Project App Factory, ChatGPT carica il registro corrente e visualizza la lista dei comandi disponibili con esempi, ambito e possibilità di modifica dei dati.

- **Sorgente canonica:** [REGISTRY.json](REGISTRY.json)
- **Vista sempre derivata:** [LEGGENDA.md](LEGGENDA.md)
- **Generatore/validatori:** `scripts/build_command_legend.py`, `scripts/test_command_legend.py`
- **Router reale:** `v27/candidate/MODULE_MAP.json` con `public_command: true`.
- **Trigger:** `Legenda` per tutta la lista; `Legenda Audit` e `Legenda Capability` per filtro testuale, mai per esecuzione.

## Aggiornare senza deriva

Quando in futuro nasce un nuovo comando, aggiungi il contratto operativo canonico e la route pubblica in MODULE_MAP, poi un'entry in REGISTRY.json, quindi esegui `python3 scripts/build_command_legend.py --write`. La CI verifica che la legenda generata sia identica, che ogni route pubblica abbia una entry nel registro, che gli ID e gli esempi non siano duplicati e che gli entrypoint esistano. La modifica richiede branch, PR e gate verdi.

La legenda non inventa macro non configurate e non esegue azioni. I comandi già esistenti hanno effetti diversi: `Audit` = sola lettura; `Capability` = scritture limitate al catalogo; `Procedi` = scope di implementazione autorizzato; `Mock-up interattivi` = iterazione design; `Integra i mock-up` = implementazione dei design approvati.

App-Factory-Core resta proprietario del registro dei COMANDI. Il registro DATI delle capability resta in Idee-app-Archivi-riferimenti.

## Comandi operativi App Factory (conteggio dinamico dal Registry)

Ogni comando ha una sorgente canonica SHA-verificata. I comandi recenti usano `commands/specs/<ID>.md`; Audit e Capability usano i rispettivi prompt completi, Mock-up e Integra i mock-up usano la policy dedicata con route distinte, Procedi usa il Core/fallback verificato. `Legenda` legge tutte le voci dal Registry senza conteggi hardcoded. Il resolver seleziona il prefisso pubblico più lungo, carica la fonte verificata e blocca contratti corrotti. Modifiche ai repository richiedono scope autorizzato e branch/PR/CI exact-head; Test/APK non pubblicano sullo Store. Questa installazione non esegue nessun workflow applicativo.

## APK e Deploy

In `Legenda` la sezione **APK e Deploy** comprende solo `APK` (Android) e `Deploy` (Web/PWA), ciascuno con specifica e SHA diversi. `Deploy <app>` è limitato a preview/staging reali; `Deploy produzione <app>` è un'intenzione pubblica esplicita, con workflow/provider già predisposti e verifica del sito online. `CI`, `Test`, `Store`, `Peso` restano in Delivery. Non parte alcuna pubblicazione durante l'installazione.
