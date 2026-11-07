# APP FACTORY — Sicurezza
Versione 1.0 | 2026-11-07 | ID: sicurezza | Effetto: SOLA LETTURA

## Scopo e sintassi

Verifica permessi, auth, segreti, backup, dati e confini di fiducia.

- Sicurezza (target dalla chat soltanto se inequivocabile).
- Sicurezza Anna's Diary (suffisso target/operazione esplicito).

## Procedura

1. Risolvi CURRENT.yaml e fissa il commit App-Factory-Core; verifica Master, Product Bible, Roadmap e Golden pertinenti senza riletture ripetitive.
2. Leggi sorgente reale, test, CI, file o altri riferimenti soltanto tramite tool/permessi disponibili; registra commit SHA, URL e provenienza.
3. Fissa SHA; controlla permessi/dati/dependency; classifica severità, prove e remediation.
4. Distingui chiaramente SOURCE, CI, device, Store, idea, decisione prodotto e ciò che è NON_VERIFICATO.
5. Consegna risultato, rischi, limiti, blocchi e prossimo passo; mai inventare esecuzione o prove.

## Limiti di autorizzazione

Nessuna mutazione del repository, PR, release, cloud, billing o workflow da un comando di consultazione.
- La parola dopo il comando non è un secondo comando. Non eseguire operazioni di un'altra route.
- Comando senza target chiaramente identificato: analisi portfolio solo quando sicura; altrimenti richiedi il minimo identificatore indispensabile.
- Non creare nuovi costi, servizi cloud, billing, cancellazioni dati o Play release senza mandato specifico e tutti i gate.
- Strumenti assenti => BLOCKED con motivo; nessun successo inventato.

## Output

Data di verifica, target, HEAD, classe di evidenza, esito, fonti e prossimi passi. Distinguere azioni proposte, in corso e concluse.

END COMMAND SICUREZZA
