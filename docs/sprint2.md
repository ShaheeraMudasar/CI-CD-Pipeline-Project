# Sprint 2 – Enhetstester och testtäckning

Den här sprinten fokuserar på att bygga vidare på pipeline-arbetet genom att införa enhetstester, coverage och skydd mot ofärdig kod. Ni kommer att fortsätta arbeta i era grupprepon med kod som ni fått förberedd av mig.

## Mål

1. Aktivera coverage-mätning i CI ([dokumentation för pytest-cov](https://pytest-cov.readthedocs.io/)):

   - Lägg till coverage-tröskel **75 %** i [pyproject.toml](../pyproject.toml)
   - [Pipeline](../.github/workflows/test.yml) ska blockeras PR merge om testtäckning <75 %

1. Skriv enhetstester i [tests/unit/](../tests/unit/) till dess att ni når testtäckningen:

   - Använd `pytest`, asserts från `pyhamcrest` samt `GIVEN`, `WHEN`, `THEN` struktur

1. (Valfritt/bonus): Lägg till så att värdet för testtäckningen syns i repots readme (genom en så kallad [badge](https://docs.codecov.com/docs/status-badges)).

## Krav

- Test-jobb ska köras automatiskt i pipeline med feedback om uppnådd coverage
- Testerna ska gå igenom
- Coverage ska vara minst 75 %
- Merge ska blockeras vid för låg täckning
- Krav från tidigare sprint (lint, PR-process) gäller fortfarande
