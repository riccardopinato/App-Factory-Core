# Donor e Reuse Passports — 08/11/2026

Registro: [donors/REGISTRO_DONOR_CAPABILITY.json](donors/REGISTRO_DONOR_CAPABILITY.json).
Passports: [reuse/PASSPORTS.json](reuse/PASSPORTS.json).

**17 progetti donatori**, **20 capability scoped**, tra cui **9 nuovi E3** provenienti da **6 progetti** con SHA/test e CI exact-head: FocusSense (due), Pocket Guard (una, shadow-only), Notification Control (due), TasteAI (due), 180FlipCharge (una), Tabletop Motion Alarm (una).

11 donor precedenti restano **legacy scoped** secondo Golden ufficiali, non ricalcolati; Send-to-PC è esplicitamente E2 data CI storica non coincidente con il main corrente. Un scope E3 non implica il funzionamento device/provider o un prodotto completo. E5 richiede una seconda adozione con prove reali.

Per riuso, si devono leggere soltanto: passport corrispondente, file sorgenti puntati e contratto Golden pertinente. Se source/test **Git blob** coincidono, mantenere prova E3 precedente e saltare l'audit donor; eseguire solo test adapter consumer. Se cambia blob, contratto, SDK, rights o sicurezza: ricontrollare quel delta. Nessuna promo globale implicita.

Non serve un secondo progetto per certificare E3. Nessuna scrittura di app, store, cloud o Play.
