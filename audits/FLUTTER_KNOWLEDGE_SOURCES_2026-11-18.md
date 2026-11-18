# Flutter Knowledge Sources — dossier operativo (18/11/2026)

Status: RESEARCH / SOURCE ROUTING ONLY — non indica package installati, donor verificati, Golden certificati o redesign approvati.
Factory baseline di partenza: `63c3ecba07dafdf46e27e175bd973ee05107fecb` (CURRENT.yaml -> Master v27, Golden Index v29).
Owner intent: interfacce 2026–27 belle, fresche, giovani, contemporanee e con qualità comparabile ai prodotti consumer leader, senza copiare asset o identità dei concorrenti.

## 1. Flutter Gems: fonte prioritaria ON-DEMAND di discovery

- Home: https://fluttergems.dev/
- Fonte: directory editoriale di package Dart/Flutter, dichiara 7.250+ package. Le categorie includono User Journey, AI/ML, funzionalità, storage, scanner/PDF, UI/theme/color, networking, social/chat, multimedia, navigation, components, scrollables, forms, text/icons, date/calendar, canvas/animation, developer tools, architecture, payment, file formats e tool di piattaforma.
- Navigazione diretta utile:
  - Design system: https://fluttergems.dev/design-system/
  - Widget library/UI framework: https://fluttergems.dev/widget-library-ui-framework/
  - Animazioni: https://fluttergems.dev/animation-transition/
  - State management: https://fluttergems.dev/state-management/
  - Testing: https://fluttergems.dev/testing/
  - Performance e crash: https://fluttergems.dev/performance-crash-insights/
  - AI/LLM: https://fluttergems.dev/chatgpt-llm-genai/
  - Rendering/generazione widget: https://fluttergems.dev/widget-generation-rendering/
- Le schede possono mostrare piattaforme supportate, compatibilità Dart, metriche di popolarità, download e uno stato di manutenzione. Alcune pagine riportano 'Last updated: May 18, 2026': NON presumere che il catalogo dia lo stato più recente a novembre.
- Limite: aggregatore terzo, non maintainers dei singoli package. Un alto ranking, stato 'Good', numero download o lista di package non convalida licensing, sicurezza, runtime, aggiornamento o compatibilità del target. Alcune categorie sono semanticamente larghe; cercare il package specifico invece di inferire capacità dal titolo.
- Consultazione: su richiesta di nuove funzioni, confronto librerie, problemi tecnici, performance o redesign Flutter; non ad ogni microfix. Prima verificare Product Bible, donor e Golden interni; per estetica prima Design-App selezionato dall'utente.
- Per ogni candidato raccogliere: URL del package su pub.dev, origine GitHub e tag/commit, licenza SPDX, Flutter/Dart SDK constraints, piattaforme, changelog e release, issue rilevanti, dipendenze transitive, costi, licenze asset, offline/privacy, dimensione binario, screenshot/demo, alternativa già in uso, test di integrazione. Se informazioni mancanti: NOT_VERIFIED.

## 2. Forui — libreria concreta, NON documentazione generica Flutter

- Source docs: https://forui.dev/docs/widgets/form/button
- Package: https://pub.dev/packages/forui
- La pagina documenta widget `FButton`, `FButton.icon`, `FButton.raw`, stili primary/secondary/destructive/outline/ghost, misure, loading, toggle, icone; mostra CLI `dart run forui style create buttons` per generare stili personalizzabili.
- L'indice Forui comprende form, overlay, navigazione, calendari, resizable layout e altro. E' candidata CODE_DONOR/LIBRARY_REFERENCE per Flutter branded multi-device, previa verifica delle API e dei vincoli SDK della versione target.
- Proposta: Design-App REFERENCE, poi micro-pilota componenti in un'app reale se compatibile con il design già approvato. NON importare l'intero framework per un pulsante e NON imporre lo stile shadcn-like a ogni app.

## 3. Flutter Gems / Medium — GenUI Sales Analytics

- Articolo: https://medium.com/@fluttergems/building-a-genui-sales-analytics-app-in-flutter-with-bring-your-own-byo-ai-model-provider-f875098d17b0
- Pubblicato il 5 maggio 2026: mostra GenUI/A2UI, catalogo di widget con schema JSON, superfici denominate, componenti custom `MetricCard`, `DonutChart`, `BarChart`, `TabularData`, `ClientFunction`, `Transport`/adapter personalizzato per Amazon Bedrock e output JSONL.
- Codice sorgente originale: https://github.com/ashitaprasad/genui_sales_analytics_app ; LICENSE Apache-2.0 presente nel repo, da preservare per eventuale riuso con attribuzione; versione dipendenza nel codice dell'esempio `genui: ^0.8.0` (non versione canonica corrente).
- L'idea riutilizzabile e' un catalogo UI dichiarativo CONFINATO ad elementi autorizzati; non un invito a far generare e eseguire codice arbitrario o a dare accesso illimitato ai dati dell'app.
- Classificazione: ARCHITECTURE/AI PATTERN DONOR + reference codice demo, NON Golden, NON feature già implementata. In possibile pilota: App Factory Agent/dashboard e analytics, Notes soltanto se funzione approvata. Richiede controllo di API GenUI, provider costs, segreti, prompt injection, autorizzazioni per tool/callback, confini dati, performance e test. Nessun AI/provider/cloud a pagamento o chiave segreta senza approvazione.

## 4. F22 Labs — confronto di 8 librerie UI, aggiornamento 2026

- Fonte: https://www.f22labs.com/blogs/top-8-flutter-ui-libraries-for-2025-you-must-explore/
- Il contenuto visibile è intitolato 'Top 8 Best Flutter UI Libraries for 2026', datato 4 agosto 2026; il path URL è rimasto '2025'.
- Otto nomi: GetWidget (componenti generalisti), shadcn_ui (UI brandizzata/SaaS), Forui (responsive touch+desktop), Mix (styling/tokens per design system), FL Chart (grafici), macos_ui (macOS), Fluent UI (Windows), TDesign Flutter (componenti business/enterprise).
- Shortlist coerente con UX proprietaria: Mix per infrastruttura token, Forui/shadcn_ui per studio componenti adattabili, FL Chart per dati; gli altri dipendono strettamente da target e limitazioni di piattaforma. Nessuno e' automaticamente 'il migliore' in tutte le app.
- Limiti della fonte: comparativa secondaria e commerciale, quindi verifica package/versioni sui siti originali, supporto piattaforma e test indipendenti. Evitare di applicare Fluent/macOS a schermi Android senza intenzione di prodotto.

## 5. GitHub Flutter Search — ricerca, non donor individuale

- Fonte: https://github.com/search?q=flutter&type=repositories
- E' una ricerca dinamica, non un elenco verificato né una licenza universale. Usarla per scoprire repo, poi restringere per lingua Dart, manutenzione, file LICENSE, test/CI, attività, SDK e rilevanza.
- Reconcile con cataloghi OSS/Stars/Donor già esistenti; deduplicare per repository canonico e commit/tag. Non attribuire automaticamente codice copiabile, golden status o stato dell'app.

## 6. Ricadute per l'ecosistema

- Anna's Diary: interfacce editoriali e personalizzate, componenti form e calendari, microinterazioni accessibili; priorità ai mock-up e al Design-App già scelti.
- Notes-Ecosistema: layout responsive, editor, ricerca, canvas, componenti dati, AI/GenUI opzionale soltanto con consenso e privacy.
- World Days: contenuti editoriali, navigazione e componenti media; non rimpiazzare il catalogo storie con pacchetti UI.
- Omni Cleaner / Battery Guard / CashMate / FocusSense: dashboards, grafici, progressi attendibili e stato operativo reale; grafici solo se migliora leggibilità.
- Wonderlog / TrailPath: mappe, immagini, navigazione, rendering fluido e target offline.
- AppLab: Flutter test, E2E native interactions, visual regression, performance/crash tools, APK size delta; nessun PASS senza esecuzione.
- Design-App: sempre FIRST per scelte di stile, reference estetiche e componenti visuali; Flutter Gems serve a trovare come implementare coerentemente, non a decidere il gusto al posto dell'utente.

## 7. Workflow e gate

1. Definisci problema, target (Android/iOS/Web/desktop), dati e Product Bible.
2. Cerca Golden/donor/code già presenti; per l'estetica consulta per primo Design-App e identifica le reference utente.
3. Se serve una soluzione esterna, cerca SOLO le categorie pertinenti in Flutter Gems; usa F22 e GitHub come confronto, Forui e tutorial come implementazioni da verificare.
4. Confronta 2–3 candidati con criteri espliciti: sicurezza/licenza, SDK compatibile, qualità prodotto e coerenza visiva, API, supporto, peso, costo, privacy, performance, accessibilità.
5. Registra SOURCE_URL, SOURCE_REPO, REF, LICENSE, classificazione (CODE_DONOR/PATTERN_DONOR/UI_REFERENCE/REJECTED), motivazione, alternativa, consumo app, test ed evidence. Un aggregatore non determina le licenze.
6. NON installare/copiare/integrare senza scope autorizzato; apri PR e valida exact-head con AppLab dove richiesto. Golden promotion ha gate separati.
7. Stato finale per ogni app: PROPOSED_ONLY / IMPLEMENTED / VERIFIED / CERTIFIED secondo prova reale; non promuovere in modo implicito.

Qualità visiva target 2026/27: tipografia, composizione, contenuto protagonista, ritmo/spazio, iconografia coerente, feedback immediato, navigazione scorrevole, stato empty/loading/offline/error, light/dark, accessibilità, jank e tempo di avvio misurati, peso APK verificato. Non usare uno stile di framework preconfezionato come identità grafica universale; non copiare grafica/branding di competitor.

Ricerca svolta: selezione di pagine e categorie, non revisione di tutti i 7.250+ package. Nessun Donor/Golden promosso e nessuna app modificata.
