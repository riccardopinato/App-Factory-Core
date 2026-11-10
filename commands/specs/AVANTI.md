# APP FACTORY — AVANTI
Versione 1.0 | 2026-11-10 | ID: avanti | Effetto: MODIFICHE SOLO NELLO SCOPE AUTORIZZATO

## Intento
`Avanti` significa: esegui il PROSSIMO PASSAGGIO OPERATIVO che è stato proposto in modo inequivocabile nella chat corrente, nel progetto corrente e nei limiti già autorizzati. Non significa "procedi su tutte le app" né autorizza una nuova scelta di prodotto.

- `Avanti`: prossimo step proposto nella chat.
- `Avanti Anna's Diary`: stesso significato limitato al target identificato.
- `Avanti roadmap` NON è un alias di questo comando: ha una route pubblica più specifica, un suo contratto e precedenza longest-prefix.

## Risoluzione del passo
1. Fissa `CURRENT.yaml` e commit SHA della Factory per questa sessione; carica solo Core, moduli/GOLDEN pertinenti, la presente specifica SHA-verificata, Product Bible e Roadmap dell'app target.
2. Identifica target, repository, ramo e UN solo prossimo passaggio concretamente proposto nella conversazione corrente (se necessario da checkpoint verificabile). Se non esiste una proposta inequivocabile, consulta la roadmap APPROVATA del target e considera il primo step fattibile; se mancano target o autorizzazione, BLOCKED_SCOPE_UNCLEAR senza inventare una decisione.
3. Riconcilia la proposta con HEAD, PR, CI e roadmap reali. Se lo step è già integrato, NON ripeterlo: passa al successivo SOLO se rimane nello scope autorizzato; altrimenti NO-OP o BLOCKED.
4. Verifica dipendenze, prerequisiti e conflitti; separa fatti IMPLEMENTED da TESTED, DEVICE/PROVIDER VERIFIED e RELEASED. Esegui solo l'azione richiesta, con i suoi controlli di sicurezza, dati, rollback e gate.
5. Per codice/roadmap: usa branch/PR, controlli pertinenti sul commit esatto, review e mergeability; merge automatico soltanto quando già autorizzato e tutti i gate richiesti sono verdi. Non interromperti per approvazioni superflue, ma non aggirare gate o decisioni irreversibili.
6. Scrivi un checkpoint finale con passo selezionato, repo+SHA, risultato, ciò che non è stato verificato, blocchi e successivo step suggerito. Non inventare esecuzioni o lavoro asincrono.

## Confini e precedenza
- Il trigger è SOLO la prima parola/il prefisso pubblico della richiesta esplicita; parole nella chat o nel contesto non autorizzano altre route.
- `Avanti roadmap` si instrada sempre a `cmd_avanti_roadmap` (prefisso pubblico più lungo), non a `cmd_avanti`.
- `Legenda Avanti` mostra il comando e non lo esegue; `Prossimo` e `Riprendi` restano consultivi.
- Un comando non approva nuove funzionalità, nuove app, cambi radicali dello stack, provider a pagamento, cancellazione dati, rilasci Store, `Deploy produzione` o nuovi privilegi.
- Non avvia lavoro in background, cron o agent autonomi. Se target, sorgenti o tool essenziali mancano: stato BLOCKED con motivo verificabile.

## Output
Target, fonte dello step (chat/roadmap), passo unico selezionato, HEAD/PR, controlli, esito (DONE/PARTIAL/BLOCKED/NO-OP), limiti e passo successivo.

END COMMAND AVANTI
