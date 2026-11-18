# Flutter Component Library — discovery prioritaria per componenti Flutter

**Data:** 19 novembre 2026 · **Classificazione:** UI_COMPONENT_DISCOVERY / REFERENCE_ONLY_PENDING_LICENSE_AND_SOURCE  
**Master:** v27 CURRENT (risoluzione da CURRENT.yaml). **Scopo:** migliorare il livello di polish delle app Flutter con componenti pertinenti, non trasformare tutte le app nel medesimo kit.

## Fonte e perimetro controllato

- Sito proposto dall'utente: https://fluttercomponentlibrary.com/ .
- La homepage ha contenuto principale renderizzato dinamicamente e non e' stata estratta integralmente dal browser di ricerca. Le seguenti **schede componenti individuali**, invece, sono state lette come testo, con titolo, categoria, descrizione, demo, percorsi dichiarati e istruzioni copy/import.
- Il testo mostrato invita a copiare il codice nell'app; **non** e' stata trovata una licenza generale identificata per la raccolta, un repo ufficiale verificato o i file Dart completi delle singole implementazioni nelle pagine accessibili. NON dedurre MIT o un permesso commerciale semplicemente perche' l'esempio e' pubblico. Le librerie omonime su pub.dev o altri domini non costituiscono prova del sito indicato.
- Percorso dichiarato nella pagina != file sorgente recuperato. Le demo iframe non sono runtime Flutter verificato su device da App Factory.
- Le descrizioni del sito («beautiful», «optimized», «responsive») sono claim del produttore, non test di prestazioni/accesibilita'/qualita' da noi eseguiti.

## Campione di 15 componenti verificati come schede pubbliche

| ID | Componente / pagina | Percorso Dart **dichiarato**, non letto | Dipendenza esplicita nella pagina | Fit possibile |
|---|---|---|---|---|
| FCL-001 | [Docking Bar](https://fluttercomponentlibrary.com/pages/components/docking-bar.html) | `lib/components/docking_bar.dart` | Non dichiarata nella scheda | Navigazione compatta, da confrontare con barra approvata |
| FCL-002 | [Custom Buttons](https://fluttercomponentlibrary.com/pages/components/custom-buttons.html) | `lib/components/custom_action_button.dart` | Non dichiarata | CTA con stile personalizzato |
| FCL-003 | [Filter Button](https://fluttercomponentlibrary.com/pages/components/filter-button.html) | `lib/components/filter_button.dart` | Non dichiarata | Filtri contestuali |
| FCL-004 | [Banner Info](https://fluttercomponentlibrary.com/pages/components/banner-info.html) | `lib/components/info_banner.dart` | Non dichiarata | Messaggi di stato e avvisi non allarmistici |
| FCL-005 | [Bottom Sheet](https://fluttercomponentlibrary.com/pages/components/bottom-sheet.html) | `lib/components/bottom_sheet_widget.dart` | Non dichiarata | Azioni e dettagli secondari |
| FCL-006 | [Book Shelf](https://fluttercomponentlibrary.com/pages/components/book-shelf.html) | `lib/components/book_shelf.dart` | Non dichiarata | Raccolte, libri/ricordi se coerente |
| FCL-007 | [Slide To Act](https://fluttercomponentlibrary.com/pages/components/slide-to-act.html) | `lib/components/slide_to_act_widget.dart` | `slide_to_act: ^2.0.2` (come dichiarato dalla pagina) | Azione deliberata, solo se accessibile |
| FCL-008 | [FAQ Widget](https://fluttercomponentlibrary.com/pages/components/faq-widget.html) | `lib/components/faq_widget.dart` | `flutter_easy_faq: ^1.0.1` | Help contestuale |
| FCL-009 | [Stepper](https://fluttercomponentlibrary.com/pages/components/stepper.html) | `lib/components/custom_stepper.dart` | `easy_stepper: ^0.8.1` | Workflow a passaggi |
| FCL-010 | [Slider](https://fluttercomponentlibrary.com/pages/components/slider.html) | `lib/components/custom_slider.dart` | Non dichiarata | Preferenze numeriche |
| FCL-011 | [Plan Card](https://fluttercomponentlibrary.com/pages/components/plan-card.html) | `lib/components/plan_card_component.dart` | Non dichiarata | Solo se esistono piani e pricing reali |
| FCL-012 | [Scratcher](https://fluttercomponentlibrary.com/pages/components/scratcher.html) | `lib/components/custom_scratcher.dart` | `scratcher: ^2.5.0` | Esperienze ludiche, non utility di sicurezza |
| FCL-013 | [Page Flipper](https://fluttercomponentlibrary.com/pages/components/page-flipper.html) | `lib/components/flip_page_widget.dart` | Non dichiarata | Pagine editoriali se leggibile/fluido |
| FCL-014 | [Drawer](https://fluttercomponentlibrary.com/pages/components/drawer.html) | `lib/components/drawer_widget.dart` | Non dichiarata | Navigazione adattiva, senza duplicazioni |
| FCL-015 | [Draggable FAB](https://fluttercomponentlibrary.com/pages/components/draggable-fab.html) | `lib/components/draggable_fab.dart` | `floating_draggable_widget: ^2.3.0` | Solo se overlay non copre contenuti/gesture |

**Nota:** «Non dichiarata» non significa «nessuna dipendenza»; le dipendenze potrebbero comparire soltanto nel sorgente integrale non esaminato. Le versioni indicate sono testuali, non verificate come compatibili col Flutter SDK corrente.

## Ordine operativo obbligatorio quando serve un componente Flutter

1. Verifica Product Bible, identita' approvata e reference preferite dall'utente in Design-App; chiari task, superfici e stati.
2. Cerca prima componenti/Golden/donor interni; confronta con widget Flutter stock gia' in uso.
3. Consulta la categoria/scheda pertinente di Flutter Component Library (poi Flutter Gems/pub.dev, Forui e altre fonti se necessario). Crea shortlist piccola, motivando il valore rispetto a una semplice widget composition.
4. Se il file Dart originale e la licenza di quel codice **sono realmente verificati**, valuta l'import source con SPDX/provenance/asset-level rights. In assenza, **non copiare**: usare come reference estetica/funzionale per nuova implementazione originale.
5. Evitare copie tali e quali che generino look AI-stock: personalizzare token (tipografia, superfici, spacings/radius, motion e icone), semantica, stati loading/empty/error/offline, dark/large-text e piattaforme.
6. Test nel repo consumer e screenshot before/after, controlli accessibilita'/fluidita'/APK/CI; un esempio trovato non e' mai una funzione gia' integrata.
7. Aggiorna Design-App per-app registri + eventuale Donor candidate solo con fonte e prova di funzionamento. Promotion Golden via Core gate dedicato.

## Selezione per-app

Vedi `riccardopinato/Design-App/UI-UX/FLUTTER_COMPONENT_LIBRARY_APP_MAP_2026-11-19.json`: 6 profili Flutter e associazioni **PROPOSED_ONLY**. La mappatura non accerta stack, versioni o schermate dei consumer e non autorizza modifiche estetiche delle Product Bible.

**Nessun componente copiato o installato; nessun Golden o consumer modificato in questa intake.**
