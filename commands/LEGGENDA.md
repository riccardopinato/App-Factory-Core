# Legenda dei comandi — App Factory

> Vista generata automaticamente da `commands/REGISTRY.json`. Non modificare questo file manualmente.

**Uso rapido:** scrivi `Legenda` in una chat collegata ad App-Factory-Core. Puoi scrivere `Legenda Audit` o `Legenda Capability` per filtrare.

## Panoramica

| Comando | Funzione | Effetto |
| --- | --- | --- |
| `Legenda` | Mostra tutti i comandi disponibili in App Factory Core, con spiegazioni ed esempi; puoi filtrare per nome. | SOLA LETTURA |
| `Stato` | Mostra commit, PR, check, release e blocchi reali per app o portafoglio. | SOLA LETTURA |
| `Prossimo` | Ordina i 5 prossimi maxi-step per impatto, urgenza, facilità, blocchi e riuso. | SOLA LETTURA |
| `Riprendi` | Recupera checkpoint, lavori incompleti, PR aperte e ultimo HEAD verificabile. | SOLA LETTURA |
| `Golden` | Verifica Registry/Index, freshness, donor, Golden candidate e gap di prova. | SOLA LETTURA |
| `Donor` | Trova e classifica implementazioni riusabili con SHA, licenza, test e delta. | SOLA LETTURA |
| `Factory` | Verifica CURRENT, Master, Registry, moduli, fallback e drift centrale. | SOLA LETTURA |
| `Adotta Factory` | Adotta standard Factory minimali preservando i workflow personalizzati. | MODIFICHE SOLO NELLO SCOPE AUTORIZZATO |
| `Audit` | Analizza lo stato reale dell'app individuata dalla chat, confrontando codice, roadmap, test, UX, sicurezza e opportunità. | SOLA LETTURA |
| `Sicurezza` | Verifica permessi, auth, segreti, backup, dati e confini di fiducia. | SOLA LETTURA |
| `Capability` | Riconcilia incrementi di codice ed evidenze per aggiornare il catalogo delle capability e le priorità per app. | SCRITTURA SOLO CATALOGO (PR + CI) |
| `Stelle` | Acquisisce nuove stelle GitHub, analizza ogni repository, estrae e deduplica funzioni, formalizza CAP E0 e kit, confronta Product Bible e produce raccomandazioni di ammissione. | SCRITTURA SOLO CATALOGO (PR + CI) |
| `Backlog` | Riordina candidate, integrate, rinviate e scartate senza perdere storia delle decisioni. | MODIFICHE SOLO NELLO SCOPE AUTORIZZATO |
| `Idee` | Deduplica idee e inserisce nuove proposte soltanto nell'inbox canonica. | MODIFICHE SOLO NELLO SCOPE AUTORIZZATO |
| `CI` | Controlla GitHub Actions, job logs, commit SHA e causa dei fallimenti. | SOLA LETTURA |
| `Test` | Pianifica e avvia, solo se autorizzato, test reali con le pipeline disponibili. | ESECUZIONE CI SENZA MODIFICHE ALLA CODEBASE |
| `Store` | Controlla readiness Play: firma, privacy, asset, versioni, test e policy. | SOLA LETTURA |
| `Peso` | Analizza APK/AAB, asset, dipendenze e ottimizzazioni misurabili. | SOLA LETTURA |
| `APK` | Verifica e, se autorizzato, produce APK con versionCode, firma e artifact controllati. | BUILD/ARTIFACT SENZA PUBBLICAZIONE |
| `Deploy` | Compila e distribuisce la parte Web/PWA tramite pipeline già configurata, distinguendo preview e produzione e verificando il sito online. | WEB DEPLOY CONTROLLATO |
| `Mock-up interattivi` | Avvia un ciclo di massimo dieci proposte di UI realmente cliccabili, una per volta con approvazione esplicita. | DESIGN INTERATTIVO; NON IMPLEMENTA IL CODICE |
| `Integra i mock-up` | Chiude il ciclo di revisione e richiede l'implementazione separata delle sole modifiche di design approvate. | IMPLEMENTAZIONE CON GATE |
| `UX` | Analizza schermate, accessibilità, navigazione, responsive e design system. | SOLA LETTURA |
| `Monetizzazione` | Analizza AdMob, Premium, lifetime, ricavi ipotizzati e policy. | SOLA LETTURA |
| `Mercato` | Confronta concorrenti, recensioni, prezzi e opportunità da fonti attuali. | SOLA LETTURA |
| `Procedi` | Prosegue la roadmap/il task già noto, applicando modalità diretta, parallela o controllata secondo rischio e autorizzazioni. | MODIFICHE SOLO NELLO SCOPE AUTORIZZATO |
| `Allinea` | Riconcilia repository e documentazione, correggendo soltanto divergenze evidence-based. | MODIFICHE SOLO NELLO SCOPE AUTORIZZATO |
| `Roadmap` | Riconcilia roadmap, completamenti reali, dipendenze e prossimi maxi-step. | MODIFICHE SOLO NELLO SCOPE AUTORIZZATO |
| `Nuova app` | Assembla bootstrap Flutter con Product Bible, roadmap, AGENTS, CI e Golden pertinenti. | MODIFICHE SOLO NELLO SCOPE AUTORIZZATO |
| `Ripara` | Individua la causa di un bug riproducibile e prepara PR minima con test. | MODIFICHE SOLO NELLO SCOPE AUTORIZZATO |

## Comandi ed esempi

### Consultazione

**Legenda dei comandi** — Mostra tutti i comandi disponibili in App Factory Core, con spiegazioni ed esempi; puoi filtrare per nome.

| Scrivi | Cosa succede |
| --- | --- |
| `Legenda` | Elenco completo e aggiornato dei comandi. |
| `Legenda Audit` | Mostra soltanto i comandi relativi ad Audit. |
| `Legenda Capability` | Mostra soltanto i comandi relativi a Capability. |

**Effetto:** SOLA LETTURA. Non esegue i comandi che elenca e non modifica repository o dati.

**Stato** — Mostra commit, PR, check, release e blocchi reali per app o portafoglio.

| Scrivi | Cosa succede |
| --- | --- |
| `Stato` | Mostra commit, PR, check, release e blocchi reali per app o portafoglio. |
| `Stato tutte le app` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

**Prossimo** — Ordina i 5 prossimi maxi-step per impatto, urgenza, facilità, blocchi e riuso.

| Scrivi | Cosa succede |
| --- | --- |
| `Prossimo` | Ordina i 5 prossimi maxi-step per impatto, urgenza, facilità, blocchi e riuso. |
| `Prossimo tutte le app` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

**Riprendi** — Recupera checkpoint, lavori incompleti, PR aperte e ultimo HEAD verificabile.

| Scrivi | Cosa succede |
| --- | --- |
| `Riprendi` | Recupera checkpoint, lavori incompleti, PR aperte e ultimo HEAD verificabile. |
| `Riprendi Anna's Diary` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

### Factory

**Golden** — Verifica Registry/Index, freshness, donor, Golden candidate e gap di prova.

| Scrivi | Cosa succede |
| --- | --- |
| `Golden` | Verifica Registry/Index, freshness, donor, Golden candidate e gap di prova. |
| `Golden Google Auth` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

**Donor** — Trova e classifica implementazioni riusabili con SHA, licenza, test e delta.

| Scrivi | Cosa succede |
| --- | --- |
| `Donor` | Trova e classifica implementazioni riusabili con SHA, licenza, test e delta. |
| `Donor Google Auth` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

**Factory** — Verifica CURRENT, Master, Registry, moduli, fallback e drift centrale.

| Scrivi | Cosa succede |
| --- | --- |
| `Factory` | Verifica CURRENT, Master, Registry, moduli, fallback e drift centrale. |
| `Factory Golden` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

**Adotta Factory** — Adotta standard Factory minimali preservando i workflow personalizzati.

| Scrivi | Cosa succede |
| --- | --- |
| `Adotta Factory` | Adotta standard Factory minimali preservando i workflow personalizzati. |
| `Adotta Factory Anna's Diary` | Variante mirata con ambito esplicito. |

**Effetto:** MODIFICHE SOLO NELLO SCOPE AUTORIZZATO. Scrivere solo con target e scope autorizzati, branch/PR, exact-head CI, review e mergeability; non cambiare feature/decisioni di prodotto.

### Verifica

**Audit 360 App Factory** — Analizza lo stato reale dell'app individuata dalla chat, confrontando codice, roadmap, test, UX, sicurezza e opportunità.

| Scrivi | Cosa succede |
| --- | --- |
| `Audit` | Audit dell'app identificabile nella chat corrente. |
| `Audit Anna's Diary` | Audit mirato ad Anna's Diary. |
| `Audit Notes-Ecosistema` | Audit mirato a Notes-Ecosistema. |
| `Audit tutte le app` | Audit trasversale del portafoglio e dei repository accessibili. |

**Effetto:** SOLA LETTURA. Non autorizza modifiche a codice, roadmap, issue o release.

**Sicurezza** — Verifica permessi, auth, segreti, backup, dati e confini di fiducia.

| Scrivi | Cosa succede |
| --- | --- |
| `Sicurezza` | Verifica permessi, auth, segreti, backup, dati e confini di fiducia. |
| `Sicurezza Anna's Diary` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

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

**Stelle → Capability complete** — Acquisisce nuove stelle GitHub, analizza ogni repository, estrae e deduplica funzioni, formalizza CAP E0 e kit, confronta Product Bible e produce raccomandazioni di ammissione.

| Scrivi | Cosa succede |
| --- | --- |
| `Stelle` | Esegui l'intera pipeline incrementale sulle stelle accessibili dell'account GitHub autorizzato. |
| `Stelle nuove` | Controlla il delta dalle stelle precedentemente inventariate e aggiorna solo le novità. |
| `Stelle 95` | Riconcilia il pacchetto storico di 95 OSS senza duplicare CAP o kit. |
| `Stelle priorità` | Confronta le candidate col prodotto e restituisce la shortlist, senza approvarla automaticamente. |
| `Stelle owner/repository` | Audit mirato a un repository indicato esplicitamente, senza presumere che sia starred. |

**Effetto:** SCRITTURA SOLO CATALOGO (PR + CI). Riuso di Capability e atlas OSS. Ricerca ammessa per tutte le licenze; copia codice non automatica. Decisioni APPROVATA/IN_ROADMAP solo con prova owner. Non modifica app, Factory, Golden o release.

**Backlog** — Riordina candidate, integrate, rinviate e scartate senza perdere storia delle decisioni.

| Scrivi | Cosa succede |
| --- | --- |
| `Backlog` | Riordina candidate, integrate, rinviate e scartate senza perdere storia delle decisioni. |
| `Backlog tutte le app` | Variante mirata con ambito esplicito. |

**Effetto:** MODIFICHE SOLO NELLO SCOPE AUTORIZZATO. Scrivere solo con target e scope autorizzati, branch/PR, exact-head CI, review e mergeability; non cambiare feature/decisioni di prodotto.

**Idee** — Deduplica idee e inserisce nuove proposte soltanto nell'inbox canonica.

| Scrivi | Cosa succede |
| --- | --- |
| `Idee` | Deduplica idee e inserisce nuove proposte soltanto nell'inbox canonica. |
| `Idee aggiungi utility per parcheggi` | Variante mirata con ambito esplicito. |

**Effetto:** MODIFICHE SOLO NELLO SCOPE AUTORIZZATO. Scrivere solo con target e scope autorizzati, branch/PR, exact-head CI, review e mergeability; non cambiare feature/decisioni di prodotto.

### Delivery

**CI** — Controlla GitHub Actions, job logs, commit SHA e causa dei fallimenti.

| Scrivi | Cosa succede |
| --- | --- |
| `CI` | Controlla GitHub Actions, job logs, commit SHA e causa dei fallimenti. |
| `CI tutte le app` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

**Test** — Pianifica e avvia, solo se autorizzato, test reali con le pipeline disponibili.

| Scrivi | Cosa succede |
| --- | --- |
| `Test` | Pianifica e avvia, solo se autorizzato, test reali con le pipeline disponibili. |
| `Test Anna's Diary` | Variante mirata con ambito esplicito. |

**Effetto:** ESECUZIONE CI SENZA MODIFICHE ALLA CODEBASE. Eseguire soltanto test autorizzati con dispatcher, head e costo noti. CI/source-only non prova fisico o store.

**Store** — Controlla readiness Play: firma, privacy, asset, versioni, test e policy.

| Scrivi | Cosa succede |
| --- | --- |
| `Store` | Controlla readiness Play: firma, privacy, asset, versioni, test e policy. |
| `Store Cooking Anime` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

**Peso** — Analizza APK/AAB, asset, dipendenze e ottimizzazioni misurabili.

| Scrivi | Cosa succede |
| --- | --- |
| `Peso` | Analizza APK/AAB, asset, dipendenze e ottimizzazioni misurabili. |
| `Peso Battery Guard` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

### APK e Deploy

**APK** — Verifica e, se autorizzato, produce APK con versionCode, firma e artifact controllati.

| Scrivi | Cosa succede |
| --- | --- |
| `APK` | Verifica e, se autorizzato, produce APK con versionCode, firma e artifact controllati. |
| `APK Anna's Diary` | Variante mirata con ambito esplicito. |

**Effetto:** BUILD/ARTIFACT SENZA PUBBLICAZIONE. Non creare segreti o firmare falsamente, non pubblicare su Store; fornire link solo dopo verifica artifact e firma.

**Deploy Web App / PWA** — Compila e distribuisce la parte Web/PWA tramite pipeline già configurata, distinguendo preview e produzione e verificando il sito online.

| Scrivi | Cosa succede |
| --- | --- |
| `Deploy` | Verifica il deploy web della app corrente, senza produzione implicita. |
| `Deploy Anna's Diary` | Controlla il deploy web di Anna's Diary e usa solo preview configurate. |
| `Deploy anteprima Anna's Diary` | Avvia una preview esistente se autorizzata e supportata. |
| `Deploy produzione Anna's Diary` | Avvia il rilascio Web pubblico solo con intent esplicito e tutti i gate. |

**Effetto:** WEB DEPLOY CONTROLLATO. Il comando base non pubblica in produzione. Nessun provider, URL o release è presunto; produzione solo esplicita con permessi/CI/source/URL verificati.

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

**UX** — Analizza schermate, accessibilità, navigazione, responsive e design system.

| Scrivi | Cosa succede |
| --- | --- |
| `UX` | Analizza schermate, accessibilità, navigazione, responsive e design system. |
| `UX Anna's Diary` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

### Business

**Monetizzazione** — Analizza AdMob, Premium, lifetime, ricavi ipotizzati e policy.

| Scrivi | Cosa succede |
| --- | --- |
| `Monetizzazione` | Analizza AdMob, Premium, lifetime, ricavi ipotizzati e policy. |
| `Monetizzazione World Days` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

**Mercato** — Confronta concorrenti, recensioni, prezzi e opportunità da fonti attuali.

| Scrivi | Cosa succede |
| --- | --- |
| `Mercato` | Confronta concorrenti, recensioni, prezzi e opportunità da fonti attuali. |
| `Mercato Cooking Anime` | Variante mirata con ambito esplicito. |

**Effetto:** SOLA LETTURA. Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.

### Esecuzione

**Prosegui il lavoro approvato** — Prosegue la roadmap/il task già noto, applicando modalità diretta, parallela o controllata secondo rischio e autorizzazioni.

| Scrivi | Cosa succede |
| --- | --- |
| `Procedi` | Continua il lavoro corrente se il contesto e la roadmap sono identificabili. |
| `Procedi con la roadmap` | Prosegue i prossimi step della roadmap effettivamente autorizzata. |
| `Continua` | Sinonimo contestuale di Procedi. |

**Effetto:** MODIFICHE SOLO NELLO SCOPE AUTORIZZATO. Non è un audit: può effettuare implementazioni solo nel perimetro già approvato, rispettando i gate GitHub.

**Allinea** — Riconcilia repository e documentazione, correggendo soltanto divergenze evidence-based.

| Scrivi | Cosa succede |
| --- | --- |
| `Allinea` | Riconcilia repository e documentazione, correggendo soltanto divergenze evidence-based. |
| `Allinea Anna's Diary` | Variante mirata con ambito esplicito. |

**Effetto:** MODIFICHE SOLO NELLO SCOPE AUTORIZZATO. Scrivere solo con target e scope autorizzati, branch/PR, exact-head CI, review e mergeability; non cambiare feature/decisioni di prodotto.

**Roadmap** — Riconcilia roadmap, completamenti reali, dipendenze e prossimi maxi-step.

| Scrivi | Cosa succede |
| --- | --- |
| `Roadmap` | Riconcilia roadmap, completamenti reali, dipendenze e prossimi maxi-step. |
| `Roadmap Anna's Diary` | Variante mirata con ambito esplicito. |

**Effetto:** MODIFICHE SOLO NELLO SCOPE AUTORIZZATO. Scrivere solo con target e scope autorizzati, branch/PR, exact-head CI, review e mergeability; non cambiare feature/decisioni di prodotto.

**Nuova app** — Assembla bootstrap Flutter con Product Bible, roadmap, AGENTS, CI e Golden pertinenti.

| Scrivi | Cosa succede |
| --- | --- |
| `Nuova app` | Assembla bootstrap Flutter con Product Bible, roadmap, AGENTS, CI e Golden pertinenti. |
| `Nuova app Habit Tracker` | Variante mirata con ambito esplicito. |

**Effetto:** MODIFICHE SOLO NELLO SCOPE AUTORIZZATO. Scrivere solo con target e scope autorizzati, branch/PR, exact-head CI, review e mergeability; non cambiare feature/decisioni di prodotto.

**Ripara** — Individua la causa di un bug riproducibile e prepara PR minima con test.

| Scrivi | Cosa succede |
| --- | --- |
| `Ripara` | Individua la causa di un bug riproducibile e prepara PR minima con test. |
| `Ripara Anna's Diary issue 42` | Variante mirata con ambito esplicito. |

**Effetto:** MODIFICHE SOLO NELLO SCOPE AUTORIZZATO. Scrivere solo con target e scope autorizzati, branch/PR, exact-head CI, review e mergeability; non cambiare feature/decisioni di prodotto.

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
