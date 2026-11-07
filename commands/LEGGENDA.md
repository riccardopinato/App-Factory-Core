# Legenda dei comandi — App Factory

> Vista generata automaticamente da `commands/REGISTRY.json`. Non modificare questo file manualmente.

**Uso rapido:** scrivi `Legenda` in una chat collegata ad App-Factory-Core. Puoi scrivere `Legenda Audit` o `Legenda Capability` per filtrare.

## Panoramica

| Comando | Funzione | Effetto |
| --- | --- | --- |
| `Legenda` | Mostra tutti i comandi disponibili in App Factory Core, con spiegazioni ed esempi; puoi filtrare per nome. | SOLA LETTURA |
| `Audit` | Analizza lo stato reale dell'app individuata dalla chat, confrontando codice, roadmap, test, UX, sicurezza e opportunità. | SOLA LETTURA |
| `Capability` | Riconcilia incrementi di codice ed evidenze per aggiornare il catalogo delle capability e le priorità per app. | SCRITTURA SOLO CATALOGO (PR + CI) |
| `Procedi` | Prosegue la roadmap/il task già noto, applicando modalità diretta, parallela o controllata secondo rischio e autorizzazioni. | MODIFICHE SOLO NELLO SCOPE AUTORIZZATO |
| `Mock-up interattivi` | Avvia un ciclo di massimo dieci proposte di UI realmente cliccabili, una per volta con approvazione esplicita. | DESIGN INTERATTIVO; NON IMPLEMENTA IL CODICE |
| `Integra i mock-up` | Chiude il ciclo di revisione e richiede l'implementazione separata delle sole modifiche di design approvate. | IMPLEMENTAZIONE CON GATE |

## Comandi ed esempi

### Consultazione

**Legenda dei comandi** — Mostra tutti i comandi disponibili in App Factory Core, con spiegazioni ed esempi; puoi filtrare per nome.

| Scrivi | Cosa succede |
| --- | --- |
| `Legenda` | Elenco completo e aggiornato dei comandi. |
| `Legenda Audit` | Mostra soltanto i comandi relativi ad Audit. |
| `Legenda Capability` | Mostra soltanto i comandi relativi a Capability. |

**Effetto:** SOLA LETTURA. Non esegue i comandi che elenca e non modifica repository o dati.

### Verifica

**Audit 360 App Factory** — Analizza lo stato reale dell'app individuata dalla chat, confrontando codice, roadmap, test, UX, sicurezza e opportunità.

| Scrivi | Cosa succede |
| --- | --- |
| `Audit` | Audit dell'app identificabile nella chat corrente. |
| `Audit Anna's Diary` | Audit mirato ad Anna's Diary. |
| `Audit Notes-Ecosistema` | Audit mirato a Notes-Ecosistema. |
| `Audit tutte le app` | Audit trasversale del portafoglio e dei repository accessibili. |

**Effetto:** SOLA LETTURA. Non autorizza modifiche a codice, roadmap, issue o release.

### Catalogo

**Sincronizzazione capability** — Riconcilia incrementi di codice ed evidenze per aggiornare il catalogo delle capability e le priorità per app.

| Scrivi | Cosa succede |
| --- | --- |
| `Capability` | Aggiornamento incrementale globale di tutte le app. |
| `Capability Anna's Diary` | Aggiornamento delle sole associazioni di Anna's Diary. |
| `Capability Agenda-per-Anna` | Variante che usa il nome del repository di Anna. |
| `Capability Notes-Ecosistema` | Aggiornamento delle capability di Notes-Ecosistema. |
| `Capability tutte le app` | Aggiornamento esplicitamente globale del registro. |
| `Capability priorità` | Riconcilia le evidenze e mostra la prossima coda operativa. |

**Effetto:** SCRITTURA SOLO CATALOGO (PR + CI). La fonte dati resta Idee-app-Archivi-riferimenti. Non modifica le singole app né promuove Golden.

### Esecuzione

**Prosegui il lavoro approvato** — Prosegue la roadmap/il task già noto, applicando modalità diretta, parallela o controllata secondo rischio e autorizzazioni.

| Scrivi | Cosa succede |
| --- | --- |
| `Procedi` | Continua il lavoro corrente se il contesto e la roadmap sono identificabili. |
| `Procedi con la roadmap` | Prosegue i prossimi step della roadmap effettivamente autorizzata. |
| `Continua` | Sinonimo contestuale di Procedi. |

**Effetto:** MODIFICHE SOLO NELLO SCOPE AUTORIZZATO. Non è un audit: può effettuare implementazioni solo nel perimetro già approvato, rispettando i gate GitHub.

### Design

**Revisione visiva interattiva** — Avvia un ciclo di massimo dieci proposte di UI realmente cliccabili, una per volta con approvazione esplicita.

| Scrivi | Cosa succede |
| --- | --- |
| `Mock-up interattivi` | Mostra il primo prototipo visivo cliccabile 1/10 dell'app corrente. |

**Effetto:** DESIGN INTERATTIVO; NON IMPLEMENTA IL CODICE. Ogni slot richiede approvazione, modifica o rifiuto; le dieci scelte non sono approvate automaticamente.

**Integra i design approvati** — Chiude il ciclo di revisione e richiede l'implementazione separata delle sole modifiche di design approvate.

| Scrivi | Cosa succede |
| --- | --- |
| `Integra i mock-up` | Termina la revisione e avvia la fase controllata di implementazione dei design approvati. |

**Effetto:** IMPLEMENTAZIONE CON GATE. Richiede scelte effettivamente approvate e rispetta roadmap, test e branch protection.

## Altri argomenti riconosciuti dal router

Queste sono parole chiave di instradamento tecnico, non comandi autonomi garantiti: richiedono contesto e non conferiscono autorizzazioni aggiuntive.

| Area | Esempi di termini |
| --- | --- |
| Factory Update | `master prompt`, `app factory core`, `regole factory` |
| Roadmap | `roadmap`, `maxi step` |
| Ui | `ui`, `ux`, `schermata`, `schermate` |
| Code | `codice`, `refactor`, `architettura`, `dipendenza` |
| Data | `database`, `dati`, `migrazione`, `migration` |
| Native | `android`, `kotlin`, `sensori`, `permessi` |
| Native Pin | `pin`, `keystore`, `biometria forte`, `biometric strong` |
| Auth | `login`, `autenticazione`, `account`, `sign in` |
| Monetization | `admob`, `pubblicita`, `premium`, `abbonamento` |
| Ai | `intelligenza artificiale`, `modello ai`, `modello locale` |
| Delivery | `ci`, `build`, `apk`, `aab` |

## Regole e aggiornamento

- `Legenda` mostra i comandi senza eseguirli; `Audit` è sola lettura; `Capability` può aggiornare soltanto il catalogo, con PR/CI; `Procedi` dipende dallo scope autorizzato.
- Per nuovi comandi: aggiornare `commands/REGISTRY.json` e dichiarare `public_command: true` nella rispettiva route di `v27/candidate/MODULE_MAP.json`. Registrare una entrypoint canonica e i gate necessari.
- Generare con `python3 scripts/build_command_legend.py --write` e verificare con `--check`. La CI blocca legende obsolete, route pubbliche non registrate e duplicati.
- Ogni chat futura deve leggere il registro sul commit Factory fissato per la sessione; non usare una legenda ricordata dalla chat come fonte più recente.
- La modifica GitHub non aggiorna da sola le istruzioni dei ChatGPT Project esterni; il pointer App Factory Core deve essere presente.
