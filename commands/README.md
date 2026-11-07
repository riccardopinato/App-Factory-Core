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

## 22 ulteriori comandi approvati (28 totali)

Ogni comando dispone di route pubblica dedicata, un contratto individuale in `commands/specs/<ID>.md` e relativo `spec_blob_sha` nel registro. `Legenda` legge le 28 voci. Il resolver seleziona un solo comando per prefisso esatto, carica la specifica verificata e blocca la richiesta quando la specifica non corrisponde all'hash. Modifiche ai repository richiedono scope autorizzato e branch/PR/CI exact-head; Test/APK non pubblicano sullo Store. Questa installazione non esegue nessun workflow applicativo.
