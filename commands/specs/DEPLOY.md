# APP FACTORY — DEPLOY WEB APP / PWA
Versione 1.0 — 07/11/2026 | ID: deploy | Effetto: WEB DEPLOY CONTROLLATO

## Intento e comandi
Gestire build, distribuzione e verifica della parte Web/PWA di una app App Factory usando esclusivamente pipeline/hosting già configurati.
- `Deploy`: risolve l'app corrente, se identificabile, e controlla possibilità ed ambiente Web.
- `Deploy <app>` o `Deploy anteprima <app>`: solo preview/staging realmente disponibile; NON pubblicare implicitamente su URL di produzione.
- `Deploy produzione <app>`: intenzione ESPLICITA di rilascio pubblico dell'app nominata. Richiede verifiche complete, autorizzazioni, ambiente e provider già configurati. Non creare nuovi progetti/hosting.
- `Legenda Deploy` filtra soltanto l'elenco: NON dispatcha.

## Procedura obbligatoria
1. Risolvi `CURRENT.yaml` e SHA Factory una volta; carica Master e Golden pertinenti dal Registry, Product Bible, Roadmap e AGENTS dell'app target.
2. Identifica repository, ref/HEAD, progetto web (Flutter Web, PWA, SPA/static), tipo di hosting e destinazione di deploy REALMENTE configurata. Non presumere GitHub Pages, Vercel, Netlify o Cloudflare. Il backend non è implicitamente incluso.
3. Preferisci `GOLDEN_CI_RELEASE_WEB_DEPLOY_FLUTTER_v2` (registry: `ci_release_web_deploy`) se adatto; per Anna's Diary esiste `riccardopinato/Agenda-per-Anna/.github/workflows/deploy-pages.yml`. `AppLab/web-preview.yml` serve la preview read-only del SOLO AppLab, non è un deployer generico.
4. Verifica sul commit corretto workflow/trigger e destinazione, asset, base-href, routing SPA, manifest/service worker PWA, environment variables pubbliche, URL canonico, secrets NON esposti e gate di test. Per Flutter usa `flutter analyze`, `flutter test`, `flutter build web --release` solo quando realmente eseguiti/autorizzati; per altri stack usa toolchain del target.
5. PREVIEW: se non esiste un ambiente separato, NON invocare workflow che pubblica su produzione. Riporta `BLOCKED_PREVIEW_UNAVAILABLE` ed esplicita che si può chiedere `Deploy produzione <app>` per la pipeline già configurata.
6. PRODUZIONE: identifica ambiente, ref/commit e domain; richiedi check exact-head, protezioni branch/environment, review, autorizzazione a costi e piano rollback. Solo il trigger di produzione autorizza un deploy pubblico, mai il semplice `Deploy`.
7. Avvia un workflow/configurazione SOLO se tool reale e permessi consentono l'azione. Se servono modifiche a workflow/provider, sono una PR separata con gate; niente nuove credenziali, DNS, backend o servizi senza decisione esplicita.
8. Rileggi workflow run, commit distribuito, environment URL restituito dalla piattaforma, raggiungibilità HTTP, risorse e smoke test. `BUILD_PASS` non equivale a `DEPLOY_VERIFIED` né a `PRODUCTION_LIVE`.
9. Se strumenti, destinazione, permessi o conferma risultano indisponibili, restituisci BLOCKED e l'azione necessaria. Non inventare URL, esito di deploy, artifact o certificazioni.

## Output
Target, repo+HEAD, ambiente (PREVIEW/PRODUCTION/UNKNOWN), workflow/provider effettivo, build/check exact-head, run URL, live URL verificato, smoke test, costi/permessi e stato (SUCCESS/FAILED/BLOCKED/NO-OP).

## Confini
- APK rimane il comando indipendente per Android; Deploy è esclusivamente Web/PWA.
- Nessun deploy avviene durante l'installazione di questo comando.
- Non si modifica Product Bible, Golden status, catalogo CAP, billing o sistemi remoti oltre all'ambiente Web espressamente autorizzato.
END COMMAND DEPLOY
