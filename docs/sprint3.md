# Sprint 3 – Integrationstester med hjälp av Localstack

Den här sprinten fokuserar på att bygga vidare på pipeline-arbetet genom att införa integrationstester. Ni kommer att använda Localstack för att testa kod mot DynamoDB-tabell utan att köra mot riktiga AWS-resurser.

## Mål

1. Skriv relevanta och vettiga integrationstester i [tests/integration/](../tests/integration/):

   - Använd `pytest`, asserts från `pyhamcrest` samt `GIVEN`, `WHEN`, `THEN` struktur
   - Använd FastAPI testclient och kör mot en DynamoDB-tabell i Localstack
     - `localstack-up` i [Makefile](../Makefile) visar hur man startar och initierar DDB tabellen i Localstack
     - `test-integ` i [Makefile](../Makefile) visar hur man kör integrationstester lokalt utan coverage med Localstack

1. Skriv färdigt [integ-test Github workflow](../.github/workflows/integ_test.yml) så att integrationstester (utan coverage!) körs i er pipeline

1. Ert [test-workflow](../.github/workflows/test.yml) ska nu endast köra [unit-testerna](../tests/unit/) (dvs inte alla tester)

1. Om det saknas, komplettera med fler enhetstester så att ert mål i unit-test coverage uppfylls

## Krav

- Integrationstester-jobb ska köras automatiskt i pipeline vid pull request och merge in i main
- Om något av workflow för lint, unit test och integrationstest misslyckas skall en PR blockeras från att kunna göra merge
- Krav från tidigare sprint (lint, PR-process, unit test coverage, etc) gäller fortfarande
