# Sprint 4 – Från CI till CD: Driftsättning till `dev`-miljön

I denna sprint tar vi det sista steget: vi utökar vår CI-pipeline till en fullständig CI/CD-pipeline. Målet är att implementera automatisk driftsättning (`deployment`) till er gemensamma `dev`-miljö i AWS. Ni kommer att konfigurera variabler och hemligheter, färdigställa ett deploy-workflow och verifiera att er applikation fungerar live.

## Mål för Sprinten

1.  **Konfigurera er `dev`-miljö:** Sätta upp alla nödvändiga variabler och hemligheter i GitHub som er pipeline behöver för att kunna prata med AWS.
2.  **Färdigställa Deploy-pipelinen:** Komplettera ert [deploy-to-dev.yml](../.github/workflows/deploy-to-dev.yml)-workflow genom att implementera de två sista, avgörande `TODO`-delarna.
    - **TODO 1:** Skicka in alla nödvändiga konfigurationsvärden till Terraform-steget.
    - **TODO 2:** Se till att End-to-End-tester körs mot den nyligen driftsatta applikationen.
3.  **Verifiera hela kedjan:** Genomföra en fullständig, lyckad driftsättning från en `git push` till en live-applikation som är taggad och verifierad i Git.

## Steg-för-steg Instruktioner

### Del 1: Förberedelser och Konfiguration

1.  **Läs och förstå:** Börja med att noggrant läsa igenom den nya informationen i [README.md](../README.md) om Sprint 4, samt koden i [deploy-to-dev.yml](../.github/workflows/deploy-to-dev.yml) och [infra/](../infra/)-katalogen. Se till att ni förstår det övergripande flödet.
2.  **Slå ihop startkoden:** Se till att er `main`-branch är uppdaterad med all startkod för Sprint 4 (Rebase, lint, test, PR, merge).
3.  **Välj ett AWS-konto:** Bestäm tillsammans i teamet **ett** av era AWS-konton som ska agera gemensamt "deployment-konto". Skriv ner detta kontots AWS Account ID.
4.  **Sätt upp variabler och hemligheter:** Gå till `Settings → Secrets and variables → Actions` i ert GitHub-repo.
    - Konfigurera alla **Variables** och **Secrets** som behövs. Ta hjälp av [infra/variables.tf/](../infra/variables.tf) för att se vad som krävs. Ni skall ha en Github secret (tänk på vilket av tf variablerna som kan anses känsligast) och resten är Github variables.
    - **VIKTIGT:** Ni ska skapa `Repository secret/variable`. I ett riktigt fall skall det skapas som olika Environments men vi gör det förenklat i denna sprint.
    - **VIKTIGT:** Börja med att sätta `DEPLOY_ENABLED` till `false`. Detta låter er testa utan att faktiskt driftsätta något.

### Del 2: Implementera och Verifiera

6.  **Färdigställ [deploy-to-dev.yml](../.github/workflows/deploy-to-dev.yml):** Nu är det dags att koda. Lös de två `TODO`-blocken i workflow-filen enligt instruktionerna.
7.  **Testkör utan deploy:** Gör en mindre ändring i koden och pusha till `main`. Eftersom `DEPLOY_ENABLED` är `false`, bör ingenting hända efter att integrationstesterna är klara.
8.  **Aktivera deployment:** Ändra `DEPLOY_ENABLED`-variabeln i GitHub till `true`.
9.  **Första riktiga deployen:** Gör en ny, liten ändring och pusha till `main`. Observera hela flödet i Actions-fliken. Om allt går som det ska, kommer ni se att en ny Git-tagg skapas i ert repo som bevis på en lyckad driftsättning!
10. **Verifiera i AWS:** Kolla i AWS console och undersök, ECR, DynamoDB, AppRunner-tjänsten och dess CloudWatch-loggar. Ni gör detta genom att antingen logga in direkt på deployment-kontot eller använd `devops1-GroupViewer`-rollen för att komma åt deployment-kontot (se [README.md](../README.md)).

### Del 3: Felsökning och Förbättring (Bonus)

11. **Simulera ett fel:** Introducera en medveten bugg i koden som gör att era E2E-tester kommer att misslyckas. Pusha ändringen. Pipelinen bör nu misslyckas på E2E-steget, och ingen Git-tagg ska skapas.
12. **Undersök felet:** Blev den trasiga versionen driftsatt? Använd `devops1-GroupViewer`-rollen för att undersöka loggarna och statusen i AppRunner.
13. **Åtgärda felet:** Gör en ny commit som fixar buggen. Pusha igen och verifiera att pipelinen nu blir helt grön och att en ny, korrekt Git-tagg skapas.

## Krav för Godkänt

- Alla Terraform-variabler ska passeras korrekt från GitHub Variables/Secrets i er pipeline.
- End-to-End-testerna ska konfigureras korrekt och köras mot den URL som AppRunner-tjänsten tillhandahåller.
- En lyckad pipeline-körning ska resultera i en ny Git-tagg i ert repository.
- Alla tidigare krav från Sprint 1-3 (linting, tester, PR-process etc.) gäller fortfarande.

## Tips för Felsökning

- **Vilka variabler behöver Terraform?** Titta i [infra/variables.tf/](../infra/variables.tf). Har variabler med default värden också fått rätt värden?
- **Vilka miljövariabler behöver E2E-testerna?** Titta i [tests/system/test_e2e_basic.py](../tests/system/test_e2e_basic.py).
- **Om deployment misslyckas:** Kontrollera logg-outputen i GitHub Actions-steget som misslyckades. Använd sedan `devops1-GroupViewer`-rollen för att titta på CloudWatch-loggarna för er AppRunner-tjänst i AWS.
- **Manuell omstart:** Du kan alltid starta om en pipeline manuellt via `workflow_dispatch` från Actions-fliken. Notera att detta kommer att använda den senaste koden på den branch du väljer.
