# Audit perenne — Unslop UI / Anti-AI 64 — azioni aperte

- **Registro:** UNSLOP-FT-2026-11-19
- **Rilevazione:** 2026-11-19
- **Stato complessivo:** INCOMPLETO — integrazione Factory di base terminata; accettazione consumer e ammissione Golden ancora aperte
- **Owner di processo:** App-Factory-Core (questo registro); owner di implementazione/QA nei repository indicati
- **Lane predefinita:** `BACKGROUND_MAINTENANCE` / `FUTURE`; non blocca nuove attività o merge di app non interessate
- **Autorità:** `CURRENT.yaml`, Master AT-01..AT-64, `contracts/UNSLOP_UI_ANTI_AI_64_BRIDGE_v1.md`, Design-App curato, Product Bible dell'app, `GOLDEN_REGISTRY.yaml`
- **Nota:** questo è un *registro di follow-up*, non una Golden né una delega a modificare l'app durante un audit di sola lettura

## Stato verificato di partenza

| Repository | Evidenza | Stato al 2026-11-19 |
|---|---|---|
| [Design-App](https://github.com/riccardopinato/Design-App/pull/56) | PR #56, DSK-011, import MIT e mappa per app | MERGED; riferimenti per cinque app ancora `PROPOSED_ONLY` |
| [App-Factory-Core](https://github.com/riccardopinato/App-Factory-Core/pull/116) | PR #116, bridge U1–U20 → AT-01…AT-64 | MERGED; nessuna Golden Unslop creata |
| [AppLab](https://github.com/riccardopinato/AppLab/pull/234) | PR #234, scanner `scripts/anti_slop_native_audit.py` e test | MERGED; scanner **euristico**, non detector completo |
| [Anna's Diary](https://github.com/riccardopinato/Agenda-per-Anna/pull/373) | PR #373, pilota di audit sorgente | MERGED; accettazione visiva/fisica **NOT VERIFIED** |
| [Android Omni Cleaner](https://github.com/riccardopinato/Android-Omni-Cleaner/pull/41) | PR #41, rifinitura Clean e prove screenshot/CI | **DRAFT OPEN**; non in main e non accettata fisicamente |

Fonte operativa e limitazioni: [bridge Core](../contracts/UNSLOP_UI_ANTI_AI_64_BRIDGE_v1.md); [audit DSK-011](https://github.com/riccardopinato/Design-App/blob/main/sources/UNSLOP_UI_AUDIT_2026-11-19.md). Non sostituire mai lo stato corrente GitHub con lo snapshot qui sopra.

## Backlog persistente e criteri di chiusura

### UNSLOP-FT-01 — Chiusura controllata pilota Omni Cleaner
- **Priorità:** P1 quando riparte la release/accettazione RC1 di Omni; altrimenti P2. **Stato:** OPEN / USER-DEVICE GATE.
- **Owner:** `riccardopinato/Android-Omni-Cleaner`, [PR #41](https://github.com/riccardopinato/Android-Omni-Cleaner/pull/41).
- **Da fare:** verificare stato reale della PR, eventuali conflitti e la policy `AGENTS.md` / freeze RC1; completare revisione UI del Clean hub, i journey critici di pulizia e l'accettazione prevista, inclusa quella fisica se richiesta; rieseguire gate exact-head dopo qualsiasi modifica.
- **Chiusura:** approvazione/accettazione richiesta ottenuta, checks sullo SHA finale PASS, screenshot comparabili approvati, merge documentato **solo se consentito dalla freeze e dai gate**. Se una verifica fisica non è disponibile mantenere `NOT_VERIFIED` e non forzare il merge.
- **Vincoli:** non toccare per errore la PR estetica parallela #40, non attenuare conferme di cancellazione, permessi, dati o messaggi di sicurezza.

### UNSLOP-FT-02 — Visual QA e accettazione su due consumer indipendenti
- **Priorità:** P1 per promozione Unslop; **Stato:** OPEN / VISUAL_NOT_VERIFIED.
- **Owner:** [Anna's Diary](https://github.com/riccardopinato/Agenda-per-Anna/pull/373) + [Omni Cleaner](https://github.com/riccardopinato/Android-Omni-Cleaner/pull/41), con evidenze AppLab.
- **Anna:** confronto con **dieci mock-up approvati** e art direction Organic iOS Journal (Rose/HSV, Manrope/Lora); screenshot reali di schermate principali e stati `empty/content/offline/error` rilevanti, font grandi, varianti light/dark quando previste; verificare accessibilità e regressioni, senza rimuovere emoji/messaggi intenzionali. PR #373 è soltanto documentazione: nessuna visual approval già implicita.
- **Omni:** baseline prima/dopo sulla superficie Clean interessata; estensione motivata a stato vuoto, azioni distruttive, light/dark, font grande e navigazione; screenshot della PR #41 già PASS per alcune configurazioni, **non** coprono la matrice completa né sostituiscono un test fisico.
- **Chiusura:** per ciascuna app registrare `repo@SHA`, fixture/viewport/locale, file screenshot reali, comparazione rispetto a reference Design-App, decisione esplicita `APPROVED/REVISE/REJECTED/NOT_VERIFIED`, QA test e gate fisico separato; due consumer realmente distinti.
- **Vincoli:** CI verde ≠ accettazione visiva; screenshot emulator ≠ dispositivo fisico; niente redesign automatico della Product Bible.

### UNSLOP-FT-03 — Taratura falsi positivi e copertura dello scanner
- **Priorità:** P2; **Stato:** OPEN / CALIBRATION_REQUIRED.
- **Owner:** [AppLab](https://github.com/riccardopinato/AppLab/pull/234), con esempi dai due consumer.
- **Baseline storica:** sullo SHA Anna `f84d335bac680a2b5e77031c6a2dd3684fb804e7` sono emersi **379 candidati euristici / 133 file**; sullo SHA Omni `3b652d57c433d23025869b8daea7e7998e9003a2` **16 candidati / 78 file Kotlin**. Non sono 395 bug o elementi da rimuovere.
- **Da fare:** classificare un campione rappresentativo U1–U20 in `KEEP_PURPOSEFUL`, `ADAPT`, `REMOVE_CANDIDATE`, `NEEDS_RUNTIME_EVIDENCE`; documentare i falsi positivi (emoji umore/compleanni, copy privacy/offline, pesi tipografici approvati, statistiche autentiche), le regole non automatizzate e la differenza fra scanner Web/native; aggiungere fixture/test solo dove migliorano affidabilità.
- **Chiusura:** report per-app riproducibile con `repo@SHA`, scanner SHA, casi etichettati e metriche di precisione **solo se calcolabili su campione definito**, regressioni testate; nessun blocco CI fondato sul conteggio grezzo.

### UNSLOP-FT-04 — Valutazione formale della promozione Golden
- **Priorità:** P2; **Stato:** OPEN / DEPENDS_ON FT-02 + FT-03 (+ FT-01 per la UI Omni in main).
- **Owner:** App-Factory-Core `golden/GOLDEN_REGISTRY.yaml`, con consumer AppLab/Design-App.
- **Da fare:** quando sono raccolte prove su due consumer indipendenti e il processo è riproducibile, valutare il livello corretto di ammissione; `COPY_READY PROCESS` e `CERTIFIED GOLDEN` non sono sinonimi, e nessuno dei due segue automaticamente da scanner/PR. Verificare i requisiti del Registry/Golden vigenti al momento della candidatura; considerare se è un Golden distinto o un'estensione del processo AppLab/Visual QA esistente, **senza duplicare le 64 regole**.
- **Chiusura:** decisione documentata `PROMOTE` o `DEFER/REJECT`, evidenze con SHA, test cross-consumer e registrazione nel Registry/Index **solo se i gate sono soddisfatti**; eventuale modifica a Master/Golden segue la normale PR con validator e fallback coerenti.
- **Vincoli:** fino ad allora **PROCESS CANDIDATE**, non Golden certificata.

## Come usarlo nei futuri audit

1. In un audit Factory trasversale, oppure di Anna's Diary, Omni Cleaner, AppLab o Design-App, leggere questo registro insieme ai soli contratti pertinenti e riconciliare i link con GitHub **in sola lettura**.
2. Per ogni ID riportare `OPEN / BLOCKED / DONE / NOT_VERIFIED`, delta rispetto alla verifica precedente, SHA/PR/evidenza, dipendenze e prossimo passo. Non confondere attività in draft, mergeti, testate e certificate.
3. **Non** ricontare come nuovo backlog i 379+16 candidati né trasformare ogni warning in un ticket senza triage. Non bloccare progetti non interessati.
4. Gli stati qui sono snapshot: chiudere un ID nel registro solo con evidence reale attraverso una PR autorizzata di manutenzione; una lettura di audit da sola non autorizza scritture.
5. La promozione Golden rimane separata dalle modifiche delle singole app. Le fonti sono i relativi HEAD e il Registry corrente, non la memoria della chat.
