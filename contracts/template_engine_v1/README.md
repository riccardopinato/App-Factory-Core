# App Factory — Template Engine Standard v1 (MAXI-STEP 1)

**Stato: CONTRACT CANDIDATE / STATIC VALIDATION ONLY.** Non è un Golden, non è un donor certificato, non è un SDK Flutter e **non è integrato** nelle 23 app. Baseline di progettazione: App-Factory-Core `2b3ae9e01764b7504980efca34f2543949dc7b89`, CURRENT Master v27 / Golden Index v29.

## Obiettivo e confini

Standardizzare **metadati e protocolli** per template **originali, nativi e su misura** per Notes, Anna, Wonderlog, TasteAI, FrameLab e altri consumer, senza forzare un medesimo storage, UI o billing provider.

- **App-owned:** l'app mantiene Product Bible, editor, owner dei dati, design tokens, preferenze, permessi e backup. App Factory fornisce **contratto comune**, non un secondo archivio centrale di note, ricordi o progetti.
- **Notion:** fonte E0/E1/E2 di ricerca e ispirazione UX. **Non** è formattazione di runtime e i ZIP/asset/testi/formule Notion di terzi **non** sono un prodotto rivendibile.
- **Applicazione:** manifest validato staticamente -> adapter approvato specifico dell'app -> preview sintetica con il rendering dell'app -> conferma -> staging -> ACL/revision check -> commit atomico su writer canonici -> ricevuta idempotente. Nessun adapter è fornito in questo step.
- **Commerciale:** categoria `access.tier` free/paid_once. `entitlement_key` è un nome logico, **non** SKU o proof of purchase. Prezzo `€3,99` è solo ipotesi di ricerca, non un campo di manifest. Per la Web/PWA occorre percorso specifico verificato.
- **Evidenza:** schema+validator+fixtures provano **forma e vincoli deterministici**, non utilizzo dell'app, correttezza del payload, screenshot, acquisto, Play/Store, persistenza crash-safe o test su dispositivo.

## Versionamento / identità

| Campo | Regola |
|---|---|
| `contract_version` | Intero `1` fisso; migrazioni a v2 richiedono versione e gate separati |
| `template_id` | Nome stabile e namespaced (`it.riccardopinato.notes.reading_library`); non cambia durante update |
| `template_version` | `MAJOR.MINOR.PATCH` senza prerelease; bump MAJOR se install/compat non retrocompatibile |
| `app_id` | Repository consumer esplicito, non implicitamente portabile tra app |
| `catalog_status` | `research_candidate` o `product_approved`; il parser **non** certifica che l'approvazione sia reale |
| `category` | Categoria canonica di indicizzazione; l'app può mostrarne una propria traduzione |
| `compatibility` | `min_app_build`, `max_app_build` opzionale, `data_contract_revision`, `required_capabilities`, `platforms` e `target_locales`. La **verifica reale** spetta all'app |
| `localization` | Titolo, descrizione, testo alternativo anteprima per ogni `target_locale`. La schema validation non valuta la qualità delle traduzioni |
| `preview` | `generated_in_app` o `bundled_original`. In quest'ultimo caso richiede path locale e SHA-256 reali; niente link remoti/token |
| `configuration` | Campi dichiarativi limitati: boolean, text, integer, choice. L'app valida sempre prima della scrittura |
| `installation` | Solo adapter app-specifico con staging/validate/atomic-commit e ricevuta per idempotenza, `removal_policy=detach_keep_user_data` |
| `access` | Free oppure paid_once con entitlement logico verificato tramite provider-agnostic Golden |
| `provenance` | Assenza di asset esterni incorporati; lista di ID TPLUX come **riferimenti di ricerca**, non licenze |

## Interfacce dell'app (da implementare in Maxi-step successivi)

Un adapter implementa le seguenti responsabilità **non codificate come import eseguibile**:

```text
AppTemplateAdapter
  supports(manifest, appBuild, dataRevision, platform, locale, capabilities)
  preview(manifest, configuration, syntheticData) -> AppNativePreview
  plan(manifest, configuration, ownerScope) -> BoundedMutationPlan
  validate(plan, currentRevision, acl, quotas, media) -> ValidationReport
  commitAtomically(plan, installReceiptKey) -> InstallReceipt
  inspectInstall(receiptKey) -> State
  removeTemplateInstance(receiptKey) -> keep_user_created_data
```

I nomi qui sono **porte concettuali**, non API Flutter già esistenti; il consumer usa writer/DB/transaction REALI. `installReceiptKey` deve incorporare almeno `ownerScope + template_id + template_version + installation_request_id`; un retry dello stesso ID non deve duplicare dati. Non usare il solo `template_id` come chiave perché due installazioni consapevolmente distinte possono essere legittime. Verificare conflitti e ACL **al commit**, non solo in preview.

## Macchina a stati della singola installazione

```text
DISCOVERED -> PREVIEWED -> CONFIGURED -> COMPATIBLE
  -> (PAID: ENTITLEMENT_VERIFIED) -> USER_CONFIRMED -> STAGED
  -> VALIDATED_AT_COMMIT -> COMMITTED -> INSTALLED
                       \\-> FAILED -> ROLLED_BACK
```

- Stato `INSTALLED` solo se commit e ricevuta idempotente sono atomici. Un download riuscito, un pagamento o la presenza del manifest **non** equivalgono a installazione.
- Sotto errore, annullamento, no-space, account switch, mismatch revision, permesso revocato o unsupported platform: nessuna modifica parziale; eventuali allegati staging eliminati dopo rollback in sicurezza.
- Installazioni esistenti non vengono riscritte automaticamente da upgrade di catalogo. Upgrade: **preview diff, staging, validazione, backup/undo quando richiesto, commit separato**.
- **Rimozione** del template da 'I miei template' scollega l'istanza dal catalogo e mantiene i contenuti creati. La cancellazione dei dati personali segue l'ordinario lifecycle dell'app, mai un erase automatico per template removal, rimborso o entitlement scaduto.
- Per `scope=shared_explicit`, il consumer deve mostrare destinatari/ruoli, chiedere consenso e verificare permessi autorevoli. Nessuna esposizione predefinita in `Noi ♡` né accesso al Private Vault.
- Offline: preview e template gratuiti già in bundle possono funzionare offline; **non promettere** uso/installazione premium non verificata. Purchases pending/failed/unknown non danno sblocco.

## Contratto store (futuro, escluso da questo step)

`CatalogManifest != StoreProduct != EntitlementSnapshot != InstallReceipt`.

Il display price deve arrivare dal provider del marketplace, non da stringhe hardcoded nel manifest. I provider rimangono per-app, e i product ID non entrano nei widget né negli export. Il Golden `GOLDEN_ENTITLEMENT_CONTRACT_FLUTTER_v1` è un contratto riusabile; non certifica Apple/Google/RevenueCat sandbox.

## Sicurezza, licenze e diritti

- Il manifest è **dati JSON declarativi**. Non accetta script, SQL, HTML eseguibile, callback, URL esterni, token, percorsi assoluti o riferimenti a ZIP Notion. Nessun template installa codice o un plugin nativo.
- `bundled_original` richiede un asset first-party con path relativo e checksum reale. Il validator controlla solo sintassi/path; integrità bytes e autorizzazione diritti devono essere verificate nell'app/package CI.
- File, backup e contenuti esterni usano il Golden candidato Import/Export: **source -> adapter -> staging -> validate -> atomic commit**, con report di perdita. **Import non è sync**.
- Tutto il contenuto premium originale deve restare utilizzabile/modificabile nei writer canonici. Il template non acquisisce ownership sui dati dell'utente e non cancella dati in seguito a revoca.
- I riferimenti `TPLUX-REF` sono un registro di ispirazione e non giustificano copia di copertine, formule, immagini, layout pixel-identici o testi di un venditore.

## Gate per il futuro

**Step 1 PASS** richiede schema valido, fixtures cross-app, validator con casi positivi/negativi, workflow Factory green e PR merged. Questo non attribuisce "COPY-READY", certificazione Golden, consumer app support o monetizzazione.

**Step 2:** prototipi app-native + approval UX per Notes/Anna/Wonderlog.
**Step 3:** un adapter reale + template gratuito su un'app, data safety e test app/QA.
**Step 4:** catalogo UI con preview e gestione installazioni (senza billing).
**Step 5:** billing provider-specific, receipt proof, restore/refund/offline state e test sandbox, solo dopo approvazione prodotto.

## Comandi di validazione

```bash
python3 scripts/validate_template_engine_v1.py
python3 -m unittest discover -s tests -p 'test_template_engine_v1.py' -v
```

Dipendenza: `jsonschema==4.26.0` già presente in `scripts/requirements.txt`.

## Dipendenze normative già disponibili

- `golden/data/GOLDEN_IMPORT_EXPORT_PORTABILITY_FLUTTER_v1_DRAFT.txt` (staging, loss reports; non copy-ready)
- `golden/data/GOLDEN_ENTITY_LIFECYCLE_TRASH_FLUTTER_v1_DRAFT.txt` (separazione remove/trashed/purge)
- `golden/monetization/GOLDEN_ENTITLEMENT_CONTRACT_FLUTTER_v1.txt` (access state provider-agnostic)
- `golden/data/GOLDEN_OFFLINE_CONTENT_PACKS_FLUTTER_v1_DRAFT.txt` (future pack integrity, non copia pronta)
- `golden/ui/GOLDEN_APP_SHELL_RESPONSIVE_VISUAL_QA_FLUTTER_v1_DRAFT.txt`
- `golden/governance/GOLDEN_PROVENANCE_REUSE_LEDGER_v1_DRAFT.txt`
- [Idea Template Store](https://github.com/riccardopinato/Idee-app-Archivi-riferimenti/blob/main/17-RICERCA-TEMPLATE-UX/IDEA_STORE_TEMPLATE_INTERNO_2026-11-09.md)

**Nessuna modifica a CURRENT, Master v27, Golden Index/Registry o Product Bible consumer.** Questo è un nuovo contratto non normativo in `contracts/` con validator mirato e CI, non una promozione Golden.
