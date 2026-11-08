# STELLE — Pipeline unica GitHub Stars → audit OSS → CAP → ammissione prodotto

Versione: 1.0 — 08/11/2026
Trigger pubblico: `Stelle`
Route: `cmd_stelle`
Mode: `CATALOG_SCOPED_WRITE / AUDIT_EVIDENCE_GATED / INCREMENTAL`
Autorità: `CURRENT.yaml` → Master v27 → Golden Registry/Index → questo contratto → Product Bible e roadmap.
Data owner: `riccardopinato/Idee-app-Archivi-riferimenti/12-CAPABILITY-E-IMPLEMENTAZIONI`.
Questo documento è un **contratto operativo per l'assistente in Chat**, non un servizio always-on, un webhook o un processo avviato da GitHub Actions senza un comando. Non simulare lavoro in background o accessi non disponibili.

## 0. Attivazione e varianti

- `Stelle`: esegui la **pipeline incrementale end-to-end** su nuove stelle GitHub dell'account autenticato `riccardopinato`; se manca il permesso alle stelle, usa le fonti di input esplicitamente fornite e presenta quel perimetro. Una lista curata precedente NON è prova di nuove stelle attuali.
- `Stelle 95`: riesamina l'insieme storico di 95 repository curati già catalogato in `AUDIT_OSS95_CAPABILITY_ATLAS_2026-11-08.json` e relativi report; NO nuovo CAP o commit se invariati.
- `Stelle owner/repository`: analizza puntualmente quel repository, anche se non risulta starred, distinguendo chiaramente la fonte dall'elenco delle stelle.
- `Stelle priorità`: riusa il censimento corrente, confronta le proposte col prodotto e restituisce una coda per app; non tocca le decisioni approvate.
- `Legenda Stelle`: consulta l'indice e la descrizione, **non** esegue la pipeline.

Non confondere `Stelle` con `Capability`: il secondo riconcilia le CAP dalle app e dai loro HEAD; il primo è una pipeline di ricerca **esterna OSS** che termina nel catalogo e riusa `capability/MASTER_CAPABILITY_SYNC_v1.txt` per registro, stati e generazione.
Una chiamata può richiedere più tool/step sincroni nella stessa conversazione. Se la finestra del turno non basta, persisti i checkpoint su branch/catalogo e riferisci il punto effettivo; NON dichiarare completo né promettere elaborazioni future.

## 1. Gate iniziale: Factory e fonti

1. Leggi una sola volta App-Factory-Core/`CURRENT.yaml` al commit corrente e fissa la baseline. Carica Master, manifest, Golden Index, Golden Registry e soltanto Golden rilevanti: single-donor admission, scoped donor catalog, provenance e reconnaissance OSS, se dichiarati applicabili. Verifica il presente spec tramite pin SHA del registro.
2. Leggi il catalogo GitHub live: `REGISTRO_CAPABILITY.json`, AGENTS, SOURCE_INVENTORY, index, matrice OSS, audit precedente, report licenze, PR/CI e app Product Bible/roadmap pertinenti. **Non presumere** 160, 199, 385, 441 o 95 come numero attuale.
3. Acquisisci le stelle dall'API GitHub **autenticata per l'identità autorizzata**, paginando `GET /user/starred?per_page=100&page=N` oppure `gh api --paginate user/starred` con login già attivo. Verifica account, token scope, completezza pagine, rate limit; salva data, fonte, count, SHA/pagine e identificatori. Non richiedere mai token in chat.
4. Se l'API non consente accesso alle stelle, **non** classificare repository curati o snapshot storici come nuove stelle live. Usa export/URL/elenco esplicitamente fornito con `source_kind=CURATED` e `stars_verification=UNVERIFIED`. Se manca un input verificabile, chiudi come `BLOCKED_STAR_INPUT` senza inventare nuove aggiunte.
5. Distingui `newly_starred_since_snapshot`, `still_starred`, `unstarred`, `unknown_snapshot`, `curated_only`. Rimuovere una stella non cancella le prove/capability acquisite.

## 2. Sorgenti incrementali e audit 100% per repository

- Normalizza `owner/repo`, canonical redirect, forks/mirror, archived, docs-only e path spostati; deduplica case-insensitive. Usa snapshot persistente, ultimo `default_branch` e HEAD. Se HEAD + documentazione/licenza invariati, riusa la prova e indica `NO_CHANGE` senza riscan profondo.
- Per ogni repository nuovo o variato acquisisci **metadati + README reale** (anche README.rst, readme.md, README.org o path dichiarato), licenza/root license e componenti, features, guida utente, API, dipendenze e documentazione disponibile. Se non riesci ad aprire una fonte, marca `EVIDENCE_GAP`; non attribuire funzionalità non documentate.
- Estrai **tutte le responsabilità funzionali distinguibili**, non una feature per progetto e non il riepilogo per sei categorie. Per ognuna: `source_repository`, `source_commit` quando verificato, `source_path`, estratto semantico sintetico, feature contract, limiti, stato di confidenza, impatto, app candidate. Più repository possono contribuire a una stessa capability.
- Distingui metadati SPDX `NOASSERTION` dal testo effettivo della licenza. **Tutti i repository possono essere analizzati come ispirazione funzionale**; il codice può essere copiato solo con licenza del file applicabile, compatibilità commerciale e attribuzione. Non considerare assenza di licenza come MIT/pubblico dominio. Source-available, GPL/AGPL, SDK commerciali, marchi e asset richiedono gate separato.
- Donor esterno resta `REFERENCE`/E0 finché SHA+path+test+licenza non autorizzano un diverso grado E1/E3. Nessuna promozione Golden o fonte app per analogia.

## 3. Deduplicazione contro il registro e codice reale

Per OGNI feature estratta:
1. Confronta ID/alias/semantica e contratto di **tutte** le CAP pertinenti del registro, non soltanto il titolo.
2. Apri l'app consumer accessibile su HEAD attuale: Product Bible, roadmap, codice, test e gap; confronta invarianti di sicurezza, data-owner, Flutter/Kotlin/Android/iOS/Web, offline-first, UX, APK footprint e manutenzione.
3. Classifica la feature come `CAP_EXISTENTE`, `ESTENSIONE_SCOPED`, `CAP_NUOVA_CONTRATTO_DISTINTO`, `OPZIONE_ARCHITETTURALE`, `FUORI_SCOPE_CONSIGLIATO` oppure `EVIDENCE_GAP`. Crea un rapporto con il delta reale; mai generare nuovi ID per sinonimi o per engine già realizzato.
4. Mappa ai consumer *solo con scope motivato*: un match tema non implica compatibilità con Anna, Notes, FocuSense o altre app. `404`/private senza accesso rende la fattibilità `DA_VERIFICARE`, non `95%`.
5. Conserva per ogni fonte i CAP esistenti collegati e le candidature E0. Riutilizza ID già ammessi (per esempio CAP-0161..CAP-0199 se riscontrati nel JSON live); il comando deve essere idempotente, senza duplicare kit, associazioni, score o stesse fonti.

## 4. Ammissione CAP E0, kit e audit prodotto

- Un nuovo `CAP-NNNN` può essere ammesso nel **catalogo come responsabilità E0** se: contratto distinto scritto, evidence path/URL, anti-dedup firmabile, nessun cap ID equivalente, consumer coerente almeno come proposta, livello `E0`, score e facilità euristici con motivazione, dipendenze e gate. ID monotono `max+1` ottenuto dal JSON live con controllo di concorrenza.
- Crea il **kit a sei file** in `13-KIT-INTEGRAZIONE/CAP-NNNN`: README, SPECIFICHE, CODICE_RIFERIMENTO.txt (può dichiarare NO_SOURCE_CODE), INTEGRAZIONE_FLUTTER, LICENZE_E_DIPENDENZE, TEST_E_VALIDAZIONE. Senza source confermato non dichiarare codice pronto, copia permessa o E3.
- Se la funzione è solo una estensione, non creare una nuova CAP salvo un **contratto autonomo, non sovrapposto e giustificato**. Traccia link `parent/extends/supersedes`; non cancellare vecchi ID né convertire un padre già implementato in `PROPOSTA`.
- Per ogni associazione nuova `app_states=PROPOSTA`, `app_product_decisions=DA_VALUTARE` e completamento `NON_IMPLEMENTATA/DA_VERIFICARE` secondo prove. Non attribuire `IN_ROADMAP` alla sola creazione dei kit o alla CI del catalogo.
- Esegui **audit di ammissione al prodotto** su tutte le nuove candidate: utilità, novità concreta, costi, fattibilità, dipendenze, licenza, compatibilità Product Bible/roadmap, rischi, valore incrementale. Registra nel catalogo **solo una raccomandazione audit**, distinta dalla `app_product_decisions` ufficiale, fra `PROPORRE_APPROVAZIONE`, `ACCORPARE`, `RINVIARE_CONSIGLIATO`, `BLOCCATO`, `FUORI_SCOPE_CONSIGLIATO`.
- Una decisione di prodotto `APPROVATA`, `RINVIATA`, `SCARTATA` o `IN_ROADMAP` richiede una decisione documentata dal product owner o Product Bible/roadmap già vigente, con fonte e data; non nasce automaticamente dal punteggio del modello. Per decisioni nuove, il comando presenta una shortlist e attende conferma esplicita in un turno successivo. Una scelta negativa non elimina la CAP dalle altre app.
- Non aggiornare roadmap app, issue app, codice app, cloud/provider, Store, Golden o Master in esecuzione di questo comando.

## 5. Commit, derivati, verifica e no-op

1. Il **solo data owner modificabile** è `riccardopinato/Idee-app-Archivi-riferimenti`: `12-CAPABILITY-E-IMPLEMENTAZIONI`, i kit `13-KIT-INTEGRAZIONE`, index/changelog e generatori strettamente pertinenti quando necessari. Il comando è catalog-scoped; non autorizza scrittura ad app, Factory, backup o account GitHub stars.
2. Salva audit per-repository e tabella repository→feature→CAP/extension→app→decisione proposta, licenze e fonte. Mantieni checkpoint e checksum della lista di input, senza includere token/segreti.
3. Modifica `REGISTRO_CAPABILITY.json` preservando tutti i precedenti `app_states` e decisioni. Ricalcola viste solo dalla source of truth: `python3 scripts/build_catalog.py`, `python3 scripts/build_catalog.py --check`, `python3 scripts/build_status_views.py --check`; esegui test catalogo e controlli su duplicati, sequenzialità CAP, associazioni e diff di stato.
4. Branch e PR limitata al catalogo; merge solo se final HEAD CI pertinente verde, branch mergeable e review obbligatorie soddisfatte. Controlla il commit su `main` e CI postmerge prima di dichiarare `INTEGRATO`.
5. Se nessun cambiamento: `NO-OP`, nessun commit, PR o file di audit datato duplicato. Se limitazioni di tempo, rate limit, permessi, licenze, schema o generatori: `PARTIAL/BLOCKED` con conteggio repository realmente esaminati, artefatti/PR effettivi e prossimo gate, senza simulare completamento.
6. In output: stelle input/nuove/verificate vs curate, numero repo/audit, feature raw vs uniche, CAP match, CAP/associazioni aggiunte, nuove app, decisioni raccomandate (non approvate), kit, punteggi, licenze, SHA/PR/CI, anomalie, 5–10 prossime opportunità per app. Priorità senza filtri percentuali predefiniti.

## 6. Casi di accettazione obbligatori

- `Stelle` non consente di affermare di aver letto le stelle correnti se l'API autenticata fallisce.
- `Stelle 95` su atlas invariato + registro già formalizzato => `NO-OP`, non creare CAP-0200..0238, non rigenerare 39 kit, non ripetere pesante audit OSS.
- Una stessa nuova capacità in 12 repository => 1 CAP e 12 fonti, non 12 CAP; 1 CAP su tre app => 3 associazioni con stati distinti.
- Sorgente AGPL/source-available/NOASSERTION => ricerca ammessa, copia codice NON implicitamente ammessa.
- Notes con engine già implementato => valutare delta specifico, non nuova seconda architettura.
- Anna con Google Calendar Direct ancora DRAFT => CalDAV rimane proposta/gate bloccato, senza OAuth né deploy.
- Una proposta per app con repo 404 => consumer `DA_VERIFICARE`; non inventare test o percentuali misurate.
- La raccomandazione `PROPORRE_APPROVAZIONE` non modifica il campo ufficiale `DA_VALUTARE`.
- `Legenda Stelle` non invoca alcun tool di mutazione del catalogo.
- CI verde sul catalogo **non** equivale a DONOR E3, APK, prova fisica, release o Golden.
- Senza tool e dati sufficienti riferisci esattamente i blocchi, mai aggiornamenti fittizi.

END STELLE v1.0
