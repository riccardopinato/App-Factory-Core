# App Factory — Spec Lite: decisione finale di adozione selettiva

**Data:** 27 novembre 2026 · **Record:** `FSL-ADOPTION-20261127` · **Esito:** **LIMITED OPT-IN, SOURCE/CI ONLY**.

**Factory baseline:** `riccardopinato/App-Factory-Core@8b3d9263ad1a72f3b8a43273550fe43646780d78`, Master v27, Golden Index v31. Il riferimento esterno `github/spec-kit` v1.4.5 resta E1, MIT; non è stato installato il tool e non si importano workflow non controllati.

## Risultati realmente misurati

| Grandezza | Prova | Interpretazione |
|---|---:|---|
| Piloti su app e agente | 3 repository, PR merge e CI post-merge GREEN | Evidenza d'uso reale del metodo su sorgenti e test, non di una pipeline AI autonoma |
| Accettazioni esplicitamente tracciate | 11 AC su 11 | Copertura di *mappatura*; ciascuna AC ha un test dedicato, non prova fisica di soddisfazione UX |
| Nuovi test di regressione piloti | 11 | Aumento documentato dei casi coperti |
| Test adapter Agent Core | 19 | Contratto source-only con scope/replay/approval/SHA |
| Test adapter AppLab | 22 | Contratto source-only con prove e identità immutable |
| Finding P2 rilevati e riparati dalla review AppLab | 4 | Prevengono falsi esiti per check non mappati, digest job/spec e identità WorkItem |
| Overhead documentale dei piloti | **462** righe di documenti contro **154** righe aggiunte tra sorgenti e test | Eccessivo per FAST: è necessario il profilo compatto |
| CI Gallery baseline vs pilot | 369s vs 362s al tentativo riuscito; primo tentativo fallito 75s | Nessuna prova di riduzione dei tempi |
| CI Omni baseline vs pilot | 315s vs 317s | Nessuna prova di riduzione dei tempi |

**Non misurati:** tempo di sviluppo umano/AI, risparmio token, FPS/latency reali dei dispositivi, throughput agentico, effettiva riduzione di bug in produzione. Non si dichiara ROI o incremento di velocità.

## Evidenze e provenance

- <https://github.com/riccardopinato/Idee-app-Archivi-riferimenti/pull/190> — ammissione OSS E1 e matrice deduplicazione su 20 processi;
- <https://github.com/riccardopinato/App-Factory-Core/pull/133> — template, schema, validatore e test;
- <https://github.com/riccardopinato/GalleryDrift/pull/19>, <https://github.com/riccardopinato/Android-Omni-Cleaner/pull/80>, <https://github.com/riccardopinato/App-Factory-Agent-Core/pull/36> — tre piloti; dati e metriche in [report Step3](pilots/2026-11-27.md);
- <https://github.com/riccardopinato/App-Factory-Core/pull/134> — ledger di prova e controlli anti-false-PASS;
- <https://github.com/riccardopinato/App-Factory-Agent-Core/pull/37> — adapter spec→WorkItem, main `117b56b20dff1e63012c314ef32a2aa80fc558ab`, [CI main](https://github.com/riccardopinato/App-Factory-Agent-Core/actions/runs/45970929150);
- <https://github.com/riccardopinato/AppLab/pull/246> — adapter spec→prova, main `0b498ef04458d56a17318823efa9e77f31cd8e4a`, [CI](https://github.com/riccardopinato/AppLab/actions/runs/45976087721), [Android](https://github.com/riccardopinato/AppLab/actions/runs/45976087592) e canary finalizzati sul commit merge.

## Decisioni operative vincolanti per il processo opt-in

**FAST — solo quando utile.** Un solo contratto compatto può contenere requisiti, scope, piano e task inline. **Non imporre** cinque documenti per una correzione banale. Il router Master DIRECT resta prioritario; nessun costo fisso addizionale se non richiesto.

**STANDARD — raccomandato selettivamente.** Usare specifica feature-scoped e AC con prove per bug riproducibili, feature con dipendenze, UI con test di regressione, integrazioni, codice condiviso e app con PR concorrenti. Ricostruire sempre scope da Product Bible/roadmap e deduplicare le PR prima di scrivere codice.

**CONTROLLED — nessuna approvazione implicita.** Rischi di migrazioni, dati privati, sicurezza, fatturazione, lifecycle e release attivano i gate del Master con human/physical/provider approval dove previsti. Un flag `APPROVED` nel JSON non è una decisione autenticata.

**Controlli fail-closed.** Nessun `validation.required_checks` senza almeno un AC assegnato; test non realizzati restano `MISSING_EVIDENCE`; SHA e digests devono combaciare con admission trusted; WorkItem, operation e target source devono essere invarianti. Il nuovo controllo nel Core impedisce l'incoerenza già in fase di validazione.

## Non promossi e ambiti esclusi

- **Nessuna nuova Golden, CAP-NNNN o Donor certificata**: mancato E2E durevole dell'agente Windows e assenza di prova di vantaggio sul throughput.
- **Nessuna adozione bulk:** non creare un manifest per ogni storia World Days o ricetta Cooking Anime, né un obbligo globale per tutte le utility.
- **Nessun secondo scheduler, verifier, approvatore, CI gate, plugin runner o publisher.** AppLab e Agent Core restano autorità preesistenti. Il software di terze parti non riceve shell con privilegi di Chat.
- **Nessun PASS runtime/DEVICE/STORE** sulla base dei test con fixture o degli screenshot automatizzati.

## Rollout e revoca

Il processo è **opt-in per singola feature**. I tre piloti esistenti costituiscono la prima wave, non una promozione di tutto il repository. Per altre app, valutare adozione solo dopo Product Bible, backlog/PR reconciliation, decisione di scope, rischio e source SHA fissati. Qualsiasi regressione di gate, tracciabilità non completa, beneficio negativo non giustificato, o nuova authority non autorizzata impone **STOP e rollback del singolo opt-in**.

La prossima verifica di valore dovrà misurare tempo umano/AI e token su feature confrontabili, oltre a un reale E2E trusted e durevole per eventuali automazioni. Questa decisione è limitata a quanto dimostrato oggi in GitHub.
