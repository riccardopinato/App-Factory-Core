# Material Design 3 — riferimento opzionale App Factory
**Data:** 19 novembre 2026  
**Stato:** REFERENCE / OPTIONAL; nessuna migrazione o scelta prodotto approvata; nessuna verifica dell'implementazione nelle singole app.

## Policy di selezione
Material 3 **non e' obbligatorio, ma non e' vietato**. Prima consultare Product Bible e design reference curate dall'utente in Design-App. L'obiettivo e' un design moderno e professionale, non uno stile stock identico per tutte le app. M3 puo' essere adottato integralmente, solo per componenti tecnici o ignorato se incoerente con l'identita' dell'app. Il framework tecnologico non decide da solo il linguaggio visivo.

## Sorgenti controllate e limiti
- Homepage: https://m3.material.io/ — pagina con rendering JavaScript, il testo completo interno non e' stato direttamente estraibile in questa acquisizione. E' catalogata come punto di accesso alla documentazione Google, NON come audit integrale di ogni pagina.
- Android/Jetpack Compose: https://developer.android.com/develop/ui/compose/designsystems/material3 — documentazione ufficiale: componenti, temi, dynamic color su Android 12+, contrasto/accessibilita', Material 3 Expressive. Versioni e API sperimentali richiedono controllo sul progetto.
- Flutter: https://docs.flutter.dev/ui/design/material e https://docs.flutter.dev/ui/widgets/material — implementazioni/ componenti Flutter; verificare la versione SDK/package effettivamente in uso. La documentazione di migrazione riporta M3 come default stilistico per Material widgets a partire da Flutter 3.16; questo NON costituisce una decisione di prodotto.
- Golden interno: golden/ui/GOLDEN_THEME_M3_FLUTTER_v1.txt (COPY-READY) e Golden Registry id `theme_m3`. La copy-readiness e' tecnica/condizionata: non obbliga a scegliere l'estetica M3 e non e' direttamente codice Jetpack Compose.

## Cosa prendere in considerazione
- Colori e semantica: tonal palettes, ruoli primary/secondary/error, dark/light, contrasto; dynamic color opzionale se coerente con brand e preferenze utente.
- Componenti: form, switch, slider, dialoghi, pulsanti, navigation bar/rail, sheet; scegliere solo quelli utili e personalizzarli quando serve.
- Motion e accessibilita': interazioni funzionali, feedback, reduced-motion, target e font scale; evitare motion decorativo.
- M3 Expressive: un'evoluzione di M3 per Android; da valutare in base a target, API e identita' dell'app, non attivare indiscriminatamente.

## Per-app — solo ipotesi da valutare nel prossimo audit
| App | Fit ipotizzato | Uso M3 | Confini |
| --- | --- | --- | --- |
| FocusSense | HIGH | impostazioni, filtri sessione, controlli e indicatori | mantenere identita' focus e dati realmente misurati |
| Tabletop Motion Alarm | HIGH | flusso armamento, countdown, interruttori, PIN | la sicurezza e l'allarme prevalgono sulla decorazione |
| The Luminous Infinite Circle | MEDIUM | preferenze accessibilita', configurazione effetti | effetti luminosi/AOD conservano identita' grafica originale e funzionamento |
| Battery Guard | MEDIUM | preferenze e riepiloghi tecnici | evitare UI generica che nasconde informazioni di batteria |

Le app nominate sono candidate estetiche, **non** dichiarazioni che utilizzino gia' Material 3; controllare prima lo stack reale nel loro repository (Kotlin/Compose o Flutter), le implementazioni e la Product Bible.

## Gate d'ammissione
1. Match della reference estetica gia' selezionata + obiettivo dell'app.
2. Confronto M3 completo / M3 personalizzato / UI proprietaria, con motivazione.
3. Controlli su compatibilita' SDK, licenza, prestazioni, peso APK, accessibilita' e platform behavior.
4. Mock-up o catture visive con approvazione e visual QA, senza confondere un compile PASS con accettazione.
5. Nessuna app modificata, nessun cambio automatico di Golden/donor o migrazione consentita da questo documento.
