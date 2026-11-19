# Professional Product Design — Anti AI-Stock Standard v1

**Date:** 2026-11-19  
**Status:** ACTIVE DESIGN POLICY COMPANION; process and expectations, NOT a certified Golden or external library.  
**Owner:** App-Factory-Core Master v27 (resolved through CURRENT.yaml).  
**Purpose:** make App Factory products look and behave as professionally designed consumer applications rather than recognizable, interchangeable AI-generated templates.

## 1. Authority and source precedence

1. Product Bible, approved screenshots/mock-ups and explicit owner taste decisions define product identity.
2. Inspect **riccardopinato/Design-App** curated references FIRST. A saved user reference has priority over aesthetic inventions from ChatGPT when suitable/adaptable; record source ID/link and DIRECT / ADAPT / NOT SUITABLE justification. Licenses, accessibility and security remain binding.
3. Reuse existing approved product-specific design tokens and compatible internal donor/Golden technical contracts; do not start from a random new design kit.
4. For unresolved visual direction, inspect original screens on Dribbble / Collect UI and sources already cataloged in Design-App (Ruixen, Uiverse, etc.). Research *the particular surface*, not the entire site.
5. For implementation consult Flutter style-neutral widget primitives (https://docs.flutter.dev/ui), official packages (https://pub.dev/), Flutter Gems category (https://fluttergems.dev/) and maintainers of any Forui/Mix/shadcn_ui/etc. package. For motion, prefer native first, Rive only for meaningful stateful design with profiling (https://pub.dev/packages/rive).
6. Support quality practices from Design-App curated DSK-001 Anti UI Slop, DSK-002 Impeccable, DSK-004 Emil Design Engineering, DSK-008 Better Interfaces and DSK-009 UI UX Pro Max. These are **design/QA references**, not automatically executable Flutter SDK code; Web hooks do not prove native UI.

External package list and example app screens are discovery/reference, never mandatory aesthetic choices. Validate source, version, platform, license, permission, binary impact, maintenance and integration tests individually. No automatic donor/Golden promotion.

## 2. Definition of an original, professional-quality app

Each app needs a meaningful distinct visual language, not merely a new accent color:
- **Audience and brand**: what users are doing; personality, contrast, accessibility, icon and copy treatment coherent with the domain.
- **Art direction**: product-specific palette (neutrals + meaningful accents where appropriate), distinctive but readable type scale, spacing rhythm, media treatment and composition.
- **Information architecture**: prioritized data and actions, predictable navigation, progressive disclosure and content density appropriate to task.
- **Interaction design**: stateful feedback, real actions, sensible gestures, transitions where they communicate direction/state, accessible focus and reduced-motion support.
- **Systematic consistency**: UI primitives, typography, corner radii, elevations, icons and motion documented as reusable tokens; screen variants follow shared logic but need not look identical.
- **Realistic polish**: populated and empty screens both look intentional; loading/permission/offline/error/retry states are truthful; images keep proper aspect ratios; forms and long localized text fit.

Do **not** imply that AI use is absent; the standard concerns observable product quality, not author identity. No detector can reliably decide from visual style alone who wrote a UI.

## 3. Visual anti-pattern review (not an unconditional blacklist)

Flag and justify any unjustified combination of:
- default blue/purple gradients, generic rounded hero cards, uniform overrounded card grid;
- randomly mixed radii, borders/shadows everywhere, glass blur, neon glow, ubiquitous pastel/purple sheen;
- generic icons, emojis used as substitute for iconography, random stock/AI illustrations, unlicensed assets;
- pseudo-bento grids with equal visual weight or arbitrary asymmetry;
- lookalike layouts across unrelated product families, empty dashboards and placeholder data presented as true;
- giant headings/hero blocks burying the user's first task, generic praise/marketing copy as UI content;
- needless animation, long delays, low-contrast labels, excess whitespace or overpacked controls;
- copied identifiable competitor appearance or visual brand.

These elements can be appropriate when the Product Bible and UX justify them. A principle is not a ban on a color, shape or framework implementation.

## 4. Lightweight workflow for substantial visual work

**A. Product brief.** Identify target users, one primary job-to-be-done, target platform, screen/state inventory, existing app baseline, constraints and approved identity.

**B. Reference-first.** List 2–3 relevant user-curated Design-App references, or explain why none fits. Cite source IDs/links and use mode (DIRECT/ADAPT/REJECT). Add examples from competitor products only when helpful; research their behavior rather than copying assets.

**C. Art direction.** Decide typography hierarchy, color semantics, spacing/radius/elevation, media style, icon set, navigation, motion and responsive behavior. Record 2–3 anti-references: e.g. 'generic violet dashboard' when inconsistent with this specific product.

**D. Propose/review.** Compare one or more meaningful app screens with content that represents real conditions, including sparse and dense states. For interactive mock-up cycles, respect the existing owner-approval/10-step contract. Do not silently integrate proposed designs.

**E. Build and visual QA.** Preserve app architecture/data/privacy. On exact-source test fixtures, review screenshot pairs, empty/populated/dark/light, long strings/large text, small/large screens and tablet/Web when targeted; verify touch/keyboard/TalkBack/VoiceOver, reduced motion, scroll performance, APK size, state truth and route discoverability. Reference `contracts/DESIGN_VISUAL_QA_PROCESS_v1.md` (IWC-01..IWC-08) and AppLab, not a new QA engine.

**F. Aesthetic acceptance.** Record reviewer disposition `APPROVED`, `REVISE`, `REJECTED` or `NOT_VERIFIED` separately from source `IMPLEMENTED`, exact-head CI and physical/store gates. If screenshots are missing, report `NOT_VERIFIED`, never visual PASS. Design strength is a review judgment supported by explicit observations and the selected references, not a fabricated objective "AI percentage".

Small isolated UI copy/accessibility fixes can use existing project design tokens and evidence without a full research cycle.

## 5. Reuse/maintenance

Store approved product-specific decisions in the app's own design/product records and Design-App app dossier (not a duplicate Product Bible). A repeatable validated pattern can be nominated for donor/Golden evaluation only with source provenance, tests and appropriate consumer evidence. Never create a single universal look for all apps.

## 6. Examples of acceptable differentiation

- **Anna's Diary:** preserve its approved personal diary art direction; editorial typography, memories with real media and calm hierarchy. Do not replace it with a generic SaaS dashboard.
- **Notes-Ecosistema:** content-first responsive workspace; robust canvas/editor and structured information density, not a page of decorative cards.
- **Android Omni Cleaner:** precise state/space reporting and trustworthy destructive-action UX; no fake progress bars or security badges.
- **World Days:** readable editorial storytelling and imagery, cultural diversity and accessible typography; not a dashboard palette repeated for every day.
- **Battery Guard / FocusSense:** measured charts and functional, legible controls; no ornamental charts or continuously running visual effects.

No app code or Golden certification is changed by this design contract.

## 7. Mandato TEAM-GRADE / Anti-AI-Template (operativo, 2026-11-19)

**Obiettivo esplicito del proprietario:** ogni app deve avere qualità percepita e robustezza confrontabili con il lavoro di un **team esperto di product design, visual/UI, UX research, content design, motion, accessibilità, ingegneria mobile, performance e QA**. Non è richiesto simulare origini o autori umani: è lecito dichiarare che si è usata l'AI. Il prodotto non deve però sembrare un collage di template generici, testi automatici, dati fittizi e controlli non rifiniti.

**Osservazione, non diagnosi di paternità:** generatori AI, kit generici e sviluppi affrettati *possono* ripetere i pattern qui censiti, ma anche sviluppatori umani; nessun elemento dimostra che una schermata è stata creata con ChatGPT, né esiste un test visivo infallibile. Non usare questo registro per attribuire autori, nascondere l'uso dell'AI o vietare indiscriminatamente gradienti, Bento, glass, framework, illustrazioni o animazioni.

**Applicabilità:** obbligatorio in nuove app, redesign significativi, mock-up di decisione, audit estetici trasversali e visual QA pre-release. Su microfix limitarsi alla regressione dello scope interessato. Product Bible e preferenze approvate sono superiori alle scorciatoie stilistiche; prima **Design-App FIRST**, poi ricerca esterna se manca un riferimento coerente. Nessuna adozione tacita di asset o licenze.

### 7.1 Checklist completa — 64 segnali e rimedi

I codici `AT-01`…`AT-64` identificano **domande diagnostiche**, non errori garantiti. Ogni segnale va verificato su schermate/stati reali; in assenza di prove è `NOT_VERIFIED`.

### A — Identità visiva e stile

| ID | Segnale da verificare | Correzione professionale |
|---|---|---|
| AT-01 | Gradienti blu/viola predefiniti | Scegliere colore e contrasto in base a identità, significato e contenuto. |
| AT-02 | Card sovrarrotondate tutte uguali | Definire una scala di raggi con differenze funzionali, non un solo raggio enorme. |
| AT-03 | Card annidate in altre card | Ridurre i livelli di contenitori e usare gerarchia, divider e spaziature. |
| AT-04 | Glassmorphism gratuito | Riservare trasparenza e blur a contesti giustificati da contenuto e contrasto. |
| AT-05 | Glow e ombre luminose indiscriminati | Ridurre rumore visivo; usare profondità solo per focus e gerarchia. |
| AT-06 | Bento usato senza logica | Dimensionare i moduli secondo priorità delle funzioni e densità dati. |
| AT-07 | Palette identiche fra prodotti diversi | Definire colori semanticamente propri per ogni Product Bible. |
| AT-08 | Accenti cromatici scelti solo per varietà | Documentare significato di colori, categorie, stati e priorità. |
| AT-09 | Icone generiche e intercambiabili | Creare vocabolario iconografico consistente, semantico e riconoscibile. |
| AT-10 | Emoji come sistema di icone | Preferire icone deliberate e accessibili; emoji solo quando hanno un ruolo esplicito. |
| AT-11 | Illustrazioni stock scollegate dalle funzioni | Usare asset pertinenti, leciti e non fuorvianti. |
| AT-12 | Cerchi, onde, sfere e forme ornamentali ripetuti | Ridurre il decoro quando sottrae spazio e chiarezza. |
| AT-13 | Sfondi complessi su ogni schermata | Proteggere il contrasto e dare priorità ai contenuti operativi. |
| AT-14 | Marchio senza identità riconoscibile | Verificare carattere riconoscibile senza dipendere dal solo nome dell'app. |
| AT-15 | Estetica di framework non personalizzata | Separare infrastruttura UI da art direction approvata e design token. |

### B — Layout, navigazione e contenuto

| ID | Segnale da verificare | Correzione professionale |
|---|---|---|
| AT-16 | Ogni schermata con lo stesso schema titolo + quattro card | Variare il layout in funzione del lavoro reale, non del template. |
| AT-17 | Dashboard scenografica senza utilità | Mostrare prima dati e azioni decision-critical. |
| AT-18 | Spazi vuoti ingiustificati | Ottimizzare densità e leggibilità soprattutto sul primo viewport. |
| AT-19 | Schermate sovraccariche | Organizzare la gerarchia e introdurre progressive disclosure utile. |
| AT-20 | Tutte le CTA visivamente primarie | Distinguere primaria, secondaria, terziaria e distruttiva. |
| AT-21 | Dati o spiegazioni duplicati fra pagine | Consolidare le informazioni e usare contesti chiari. |
| AT-22 | Navigazione lunga o imprevedibile | Ridurre tap, preservare back stack e coerenza fra destinazioni. |
| AT-23 | Accordion ovunque con effetto timeline | Preferire schermate dedicate quando hanno workflow e contenuto autonomi. |
| AT-24 | Gerarchia tipografica piatta | Documentare scala, pesi, allineamenti e priorità dei dati. |
| AT-25 | Font, interlinea e pesi lasciati ai default | Scegliere tipografia leggibile e distintiva, con fallback robusto. |
| AT-26 | FAB o overlay che coprono azioni | Verificare insets, tastiera, banner, dimensioni e collisioni. |
| AT-27 | Header sovradimensionati | Dare accesso immediato alla prima azione o informazione utile. |
| AT-28 | Layout valido solo sul dispositivo del mock-up | Testare larghezze, font scaling, landscape quando previsto. |

### C — Motion, feedback e fluidità

| ID | Segnale da verificare | Correzione professionale |
|---|---|---|
| AT-29 | Animazioni applicate a ogni elemento | Animare solo cambi di stato, gerarchia e transizioni utili. |
| AT-30 | Rimbalzi, rotazioni e slide gratuiti | Scegliere motion coerente con compito e direzione. |
| AT-31 | Animazioni lente che bloccano il compito | Mantenere input pronto e transizioni brevi e interrompibili. |
| AT-32 | Loader scenografici privi di informazioni | Mostrare lavoro reale, risultato, stop o retry. |
| AT-33 | Progresso percentuale inventato | Usare avanzamento determinato solo se misurabile. |
| AT-34 | Transizioni diverse per flussi equivalenti | Definire un motion system con durate, easing e contesto. |
| AT-35 | Effetti di ingresso ripetuti a ogni navigazione | Ridurre ripetizioni; consentire interazione immediata. |
| AT-36 | Reduced motion ignorato | Prevedere fallback senza animazione e preferenze di accessibilità. |
| AT-37 | Scroll e navigazione con jank | Misurare frame time, allocazioni e workload reale. |

### D — Testi, localizzazione e credibilità

| ID | Segnale da verificare | Correzione professionale |
|---|---|---|
| AT-38 | Microcopy promozionale generico | Scrivere testi concreti legati a funzione, beneficio e stato verificabile. |
| AT-39 | Entusiasmo automatico e complimenti gratuiti | Usare tono umano, sobrio e adatto al contesto. |
| AT-40 | Paragrafi didascalici inutili | Usare etichette concise e aiuto contestuale dove serve. |
| AT-41 | Gergo pseudo-tecnico privo di funzione | Rimuovere AI-Powered/Ultra/Smart se non sostenuto da capability reale. |
| AT-42 | Stesse frasi ripetute in schermate diverse | Scrivere contenuti specifici per fase e destinazione. |
| AT-43 | Pulsanti etichettati Scopri/Continua senza oggetto | Indicare azione e conseguenza in forma inequivoca. |
| AT-44 | Traduzioni letterali e testi non adattati | Verificare idiomaticità, pluralizzazione, lunghezza e fallback. |
| AT-45 | Successi dichiarati prima della conferma | Basare messaggi su stato verificato, non su chiamata API avviata. |

### E — Comportamento reale, stati ed etica

| ID | Segnale da verificare | Correzione professionale |
|---|---|---|
| AT-46 | Grafici o dati demo presentati come reali | Etichettare fixture e mostrare solo dati effettivi in produzione. |
| AT-47 | Stati vuoti trascurati | Progettare first-run, zero contenuti e prossimo passo reale. |
| AT-48 | Errori generici senza recovery | Spiegare problema, impatto, retry o alternativa. |
| AT-49 | Comandi senza feedback | Fornire stato, esito e disponibilità delle azioni. |
| AT-50 | Feature aggiunte per impressionare | Rimuovere o rinviare ciò che non migliora il job-to-be-done. |
| AT-51 | Conferme distruttive deboli | Mostrare oggetto, conseguenza, reversibilità e consenso esplicito. |
| AT-52 | Wizard e passaggi eccessivi | Ridurre frizione senza rimuovere gate necessari. |
| AT-53 | Contrasto, touch e TalkBack trascurati | Verificare semantica, lettori schermo, >=48dp ove applicabile. |
| AT-54 | Comportamenti UI incoerenti fra schermate | Definire stati, componenti e feedback condivisi. |
| AT-55 | Stati reali complessi non collaudati | Testare permessi negati, offline, dati massivi, media e testi lunghi. |

### F — Qualità del codice e rilascio

| ID | Segnale da verificare | Correzione professionale |
|---|---|---|
| AT-56 | Componenti UI duplicati | Riusare primitive condivise senza creare architetture astratte superflue. |
| AT-57 | Token grafici hardcoded e incoerenti | Centralizzare colori semantici, spaziature, raggi, motion e tipografia. |
| AT-58 | Dipendenze decorative inutili | Verificare costo, manutenzione, sicurezza, licenza e dimensione build. |
| AT-59 | Animazioni senza profiling | Misurare FPS, carico CPU/GPU, autonomia e reduced motion. |
| AT-60 | Mock-up senza QA su dispositivi reali | Separare screenshot/CI da accettazione fisica. |
| AT-61 | Codice sovra-ingegnerizzato per UI banali | Preferire componenti semplici, testabili e già posseduti. |
| AT-62 | Correzioni estetiche incoerenti fra pagine | Applicare token e QA visivo trasversale, senza scope creep. |
| AT-63 | Restyling che rompe feature o dati | Eseguire regression test per navigazione, storage e flussi critici. |
| AT-64 | Direzione artistica non documentata | Conservare brief, reference Design-App, decisioni e changelog. |


### 7.2 Dieci controlli prioritari (gate estetico)

| Ordine | Controllo | Codici di riferimento |
|---|---|---|
| 1 | Identità visiva distinguibile dai template | AT-07, AT-14, AT-15, AT-64 |
| 2 | Decorazioni, gradienti e sfondi giustificati | AT-01, AT-04, AT-05, AT-12, AT-13 |
| 3 | Gerarchia di compito, dati e CTA | AT-17, AT-20, AT-24, AT-28 |
| 4 | Niente ripetizione meccanica di card/componenti | AT-02, AT-03, AT-06, AT-16 |
| 5 | Microcopy naturale e informativo | AT-38, AT-39, AT-41, AT-43 |
| 6 | Motion proporzionato e FPS verificabili | AT-29…AT-37 |
| 7 | Informazione visiva densa senza caos | AT-18, AT-19, AT-23, AT-27 |
| 8 | Stati reali: first-run, errore, attesa, permessi | AT-33, AT-34, AT-46…AT-55 |
| 9 | Iconografia e tipografia intenzionali | AT-09, AT-10, AT-24, AT-25 |
| 10 | Coerenza trasversale e assenza di regressioni | AT-54, AT-56, AT-57, AT-62, AT-63 |

**Ordine operativo:** correggere prima i rischi per fiducia, sicurezza, accessibilità, contenuti falsi e blocco dei flussi; poi gerarchia/usabilità; infine polish soggettivo. I codici non impongono automaticamente severità P0/P1/P2: assegnarla in base a evidenza e impatto utente.

### 7.3 Contratto di revisione e accettazione

Per ogni schermata o flusso campionato riportare:
1. **Provenienza:** repo + source SHA + schermo/stato + piattaforma/viewport; Product Bible e riferimento Design-App (ID, URL, DIRETTA/ADATTATA/NON ADATTA).
2. **Diagnosi:** codici `AT-xx`, osservazione specifica (con screenshot reale, test o frammento di codice), impatto e motivazione; `FOUND`, `NOT_FOUND`, `NOT_APPLICABLE` con motivazione, o `NOT_VERIFIED`.
3. **Scelta designer:** mantenere, migliorare, rimuovere, o rifiutare la proposta; indicare direzione artistica, token, gerarchia, comportamento, testo e densità desiderati. Controllare almeno due alternative solo quando davvero servono.
4. **Responsabilità team virtuale:** Product (job e scope), Visual (identità e sistema), UX/Content (comprensibilità e journey), Engineering (feasibility e regressioni), Accessibilità (semantica e large type), QA (stati e form factor), Performance (jank/batteria/peso). Sono **prospettive di revisione**, non persone/agenti realmente operanti se non esistono.
5. **Evidenza prima/dopo:** screenshot stessi dati/fixture/viewport (light/dark, 360dp e large font quando applicabile), TalkBack/contrasto/touch, loading/empty/error/offline/permission, navigazione Back, motion ridotto, profilo prestazioni e dimensione APK dove pertinente.
6. **Gate e verità:** `SOURCE_IMPLEMENTED` non è `VISUAL_APPROVED`; CI verde non certifica resa su dispositivo. Approvazione estetica esplicita, QA runtime e certificazione release restano stati distinti; senza screenshot o test rilevanti, `NOT_VERIFIED` e non `PASS`.

Nessun mock-up inventato può dimostrare la qualità runtime. Non cambiare permessi, dati, cleanup, sync, billing, licenze o stack per inseguire un effetto visivo. Un controllo che non trova difetti può essere registrato come `NO_CHANGE`, anziché creare lavori o dipendenze artificiali.

### 7.4 Regola decisionale finale

> Prima di implementare un elemento visivo, rispondere: **qual è il suo scopo di prodotto?** Serve a identità approvata, gerarchia, comprensione, fiducia, accessibilità, navigazione o feedback reale? Se la sola risposta è “rende il mock-up più appariscente”, non è sufficiente per l'approvazione. Favorire composizioni curate, sobrie quando utile e caratteristiche del prodotto, anziché effetti generici.

**Fonte dei 64 segnali:** elenco operativo concordato in conversazione il 19/11/2026, non classificazione empirica universale o attestazione di origine AI. Questo documento è un contratto di qualità/revisione, non un detector, un Golden certificato o un'autorizzazione autonoma ad alterare ogni app.

## 8. Unslop UI — subtrattiva, source-aware (2026-11-19)

Il Master v27 richiama questo contratto per il gate AT-01..AT-64. Per applicare i controlli U1–U20 dello strumento MIT `felipebasurto/unslop-ui` senza duplicare o rinumerare i 64 segnali, usare il bridge [UNSLOP_UI_ANTI_AI_64_BRIDGE_v1.md](UNSLOP_UI_ANTI_AI_64_BRIDGE_v1.md). Il conteggio regex e' solo triage; qualsiasi rimozione richiede revisione semantica, fonte/stato reali, localizzazioni, Product Bible e reference Design-App. Flutter/Dart e Kotlin/Compose richiedono adattatore e screenshot native indipendenti; nessuna approvazione visiva o Golden certificata e' implicita.
