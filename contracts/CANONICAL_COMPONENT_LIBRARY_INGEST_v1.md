# App Factory — Canonical Component Code Library ingestion contract v1
**Date:** 2026-11-19 · **Authority:** CURRENT.yaml, active Master v27, App-Factory-Core Golden/Donor admission rules.

## Scopo e autorita'
La nuova libreria dentro **riccardopinato/Design-App/BIBLIOTECA_COMPONENTI/** e' l'unico punto di ricerca trasversale per componenti UI/UX scoperti in Uiverse, Flutter Component Library, Flutter Gems, Forui, Ruixen, DevLibraries e altre fonti curate. Non creare duplicati di cataloghi per sito, né spostare Product Bible/Golden source of truth. **Design-App dell'utente e Product Bible precedono sempre qualunque estetica prefabbricata**.

## Regola generale di acquisizione
Quando il codice sorgente di un componente interessante e' realmente disponibile e con diritti di riuso verificati, **archiviarlo direttamente** in formato nativo (Dart, Kotlin, TSX, HTML, CSS, SVG, ecc.), come fonte pinned, con ID, URL, originale path, commit/source blob SHA, license/NOTICE e dipendenze dichiarate. Copiarlo in un file .md non lo rende piu' leggero, meno coperto da diritti o eseguibile in un linguaggio diverso. Mantenere una sola copia fisica e puntarla dal catalogo. Acquisire in lotti coerenti, con controllo commit SHA, evitando che il repository cresca con duplicati o media non necessari.

Quando e' visibile solo una pagina, una demo o una scheda che dichiara un percorso sorgente non recuperato, la voce e' **REFERENCE_ONLY**. Un sito pubblico che dice "copy" non dimostra automaticamente diritti commerciali, diritti sugli asset, disponibilita' dei file o funzionamento. Non incorporare codice di terzi privo di autorizzazione verificabile; registrare URL e implementare autonomamente il pattern utile se necessario. L'assenza di una fonte non deve bloccare l'indicizzazione delle altre fonti autorizzate.

## Identita', dedup e indicizzazione
- Conservare ID canonici esistenti (UIV/FCL/AMX/WML/...) e introdurre ID stabili per nuovi provider. Le schede storiche diventano **alias**, non record duplicati, quando l'origine/file identico e' verificato o una mappatura canonica e' gia' documentata.
- Distinguere identita' visiva, nome e fonte di codice: somiglianza del titolo non prova codice identico. Il fingerprint originale repo@commit:path e gli SHA/blob sono evidenze valide, con cautela se un file contiene piu' export.
- Metadati minimi: categoria, lingua/stack, fonte originale, diritti verificati, sorgente locale o `REFERENCE_ONLY`, app candidate, stato di verifica e link di documentazione.
- Usare `BIBLIOTECA_COMPONENTI/cerca.py` e il catalogo JSON per ricerca in sola lettura. Se si aggiorna il codice, conservare la versione/sha storico o documentare chiaramente la sostituzione.
- Rispettare il workflow e i validatori in Design-App; lo stato `ARCHIVED_SOURCE` non e' `COPY_READY`.

## Esempio di normalizzazione verificata (19/11/2026)
Nel PR Design-App #48, 277 componenti Ruixen TSX originali sono stati importati da `ruixenui/ruixen.com@f6b20860623fa39122ac2b5f0e5bd29a9eb10941` con hash Git verificati e MIT conservata. I 111 snippet Uiverse HTML/CSS gia' archiviati sono referenziati senza doppie copie. L'indice censisce 478 voci canoniche e 4 alias; le voci prive di originale disponibile restano REFERENCE_ONLY. Questi numeri sono lo snapshot di data audit, **non limiti fissi del Master**.

## Riuso tecnico e visual QA
Il file copiato rimane un sorgente originale: TSX/React non diventa Flutter, e un modulo HTML/CSS non ha comportamento native Android. Prima di un riuso scegliere stile e Product Bible dell'app, controllare SDK, versioni pacchetti, permessi, peso APK, accessibilita', riduzione motion, resilienza loading/empty/offline/error, dati reali e sicurezza. Testare codice, screenshot e dispositivo; mantenere distinti `SOURCE_ARCHIVED`, `SOURCE_VERIFIED`, `LIBRARY_VERIFIED`, `COPY_READY` e `CONSUMER_VERIFIED`. La promozione Golden e' separata e richiede i gate del Registry.

## Ambito di questa regola
Biblioteca e governance, non installazione in consumer, non approvazione estetica e non certificazione automatiche. Aggiornare le schede e la sezione Design-App ad ogni nuovo intake; correggere errori di provenienza prima del merge. Conservare license/NOTICE e attribution quando richiesto e rispettare diritti d'autore/asset.
