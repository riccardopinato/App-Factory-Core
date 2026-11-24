# Lean Engineering — App Factory v1 (24/11/2026)

**Stato:** policy operativa nel Master v27; metriche e vantaggi ancora **NON CERTIFICATI**.
**Riferimento operativo:** `v27/candidate/modules/90-lean-engineering.txt` (policy update del Master v27). La sezione legacy 10.1 e il Code Hygiene Golden restano invariati nel loro perimetro certificato.
**Ispirazione:** [Ponytail](https://github.com/DietrichGebert/ponytail), licenza MIT.
Le regole seguenti sono adattate all'App Factory: non richiedono installare il
plugin, non promettono gli stessi benchmark e non creano una seconda authority.

## Scopo e priorita'

Produrre la minima implementazione **completa**, non il minor numero possibile
di righe. Product Bible, requisiti approvati, Design-App, Golden appropriati,
privacy e sicurezza, AppLab, firma e limiti operativi prevalgono sulle
ottimizzazioni. Il Fast Track IA continua a usare lotti grandi e parallelismo
reale quando le unita' sono indipendenti.

## Procedura

1. **Mappa il flusso necessario:** risultato osservabile, utenti, chiamanti,
   persistenza, test, configurazione, errori e dati che possono andare persi.
2. **Ricerca locale prima:** codice e design system dell'app; poi Golden
   certificati/copy-ready pertinenti, Donor interni, API standard/native e
   dipendenze gia' installate. Le fonti OSS esterne richiedono confronto solo
   quando i vantaggi attesi giustificano il costo; registrare provenienza/licenza.
3. **Scegli la prima soluzione completa:** estendi o configura, altrimenti
   aggiungi codice minimo leggibile e coerente con l'architettura esistente.
   Nessuna nuova astrazione, stato, database, dipendenza o opzione per un
   futuro ipotetico. Un Golden non forza la sostituzione di codice locale
   migliore e gia' testato.
4. **Implementa senza restringere lo scope:** sistema chiamanti e fixture,
   copri rami/failure path significativi, conserva validazioni alle trust
   boundary e le operazioni di recupero. Parallelizza solo stream indipendenti.
5. **Review delimitata:** nel sottosistema toccato cerca duplicati, codice
   superseded, dipendenze, asset e workaround obsoleti; preserva migrazioni,
   dati, compatibilita' e storia senza evidenza di rimozione sicura.
6. **Convalida il risultato finale:** test pertinenti dopo cleanup, PR/CI
   exact-head, AppLab e physical/store gate quando applicabili. Non trasformare
   NON VERIFICATO in PASS.
7. **Rendi visibile la scelta:** riuso effettivo, codice/dipendenze aggiunte,
   parti ragionevolmente omesse e rischi o verifiche non eseguite.

### Esempio — anteprima video Omni Cleaner

Prima verificare player, controller, navigazione e permessi gia' presenti.
Se sono compatibili, aggiungere gesture e overlay riutilizzando lo stesso
controllo di cancellazione, senza creare un secondo media store. Testare
long-press, scroll, formati non validi, eliminazione e ripristino. Non
accorciare i test di perdita dati.

### Esempio — contenuti World Days

Per 600 record indipendenti, mantenere inventario canonico, lotti da 100,
parallelismo sicuro, controlli editoriali proporzionati e import idempotente.
Lean significa evitare analisi, report e build ripetute per ogni singolo record,
non processare solo 5 record per volta.

## Advisory metrics per i piloti

Per ogni PR pilota raccogliere, **senza nuovi gate di merge**:
- file toccati, righe aggiunte/eliminate (separando generated/lockfiles);
- nuove dipendenze e giustificazione; componenti riutilizzati con provenienza;
- test nuovi/aggiornati, regression check e risultati trusted;
- eventuali tempi/token/costi solo con telemetria reale e comparabile.

Le metriche su righe o test presenti nel diff NON sono prove di qualità,
copertura, efficacia o risparmio. Rapporto suggerito: baseline, commit,
cosa e' stato riusato, diff, controlli PASS/FAIL/NOT VERIFIED, rischi.
