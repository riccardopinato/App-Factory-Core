# APP FACTORY — Idee
Versione 1.0 | 2026-11-07 | ID: idee | Effetto: MODIFICHE SOLO NELLO SCOPE AUTORIZZATO

## Scopo e sintassi

Deduplica idee e inserisce nuove proposte soltanto nell'inbox canonica.

- Idee (target dalla chat soltanto se inequivocabile).
- Idee aggiungi utility per parcheggi (suffisso target/operazione esplicito).

## Procedura

1. Risolvi CURRENT.yaml e fissa il commit App-Factory-Core; verifica Master, Product Bible, Roadmap e Golden pertinenti senza riletture ripetitive.
2. Leggi sorgente reale, test, CI, file o altri riferimenti soltanto tramite tool/permessi disponibili; registra commit SHA, URL e provenienza.
3. Confronta inbox/portfolio/CAP; registra origine e ID monotono; PR solo per aggiunta esplicita.
4. Distingui chiaramente SOURCE, CI, device, Store, idea, decisione prodotto e ciò che è NON_VERIFICATO.
5. Consegna risultato, rischi, limiti, blocchi e prossimo passo; mai inventare esecuzione o prove.

## Limiti di autorizzazione

Scrivere solo con target e scope autorizzati, branch/PR, exact-head CI, review e mergeability; non cambiare feature/decisioni di prodotto.
- La parola dopo il comando non è un secondo comando. Non eseguire operazioni di un'altra route.
- Comando senza target chiaramente identificato: analisi portfolio solo quando sicura; altrimenti richiedi il minimo identificatore indispensabile.
- Non creare nuovi costi, servizi cloud, billing, cancellazioni dati o Play release senza mandato specifico e tutti i gate.
- Strumenti assenti => BLOCKED con motivo; nessun successo inventato.

## Output

Data di verifica, target, HEAD, classe di evidenza, esito, fonti e prossimi passi. Distinguere azioni proposte, in corso e concluse.

END COMMAND IDEE
