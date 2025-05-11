# Sprint 1

## Mål

1. Skapa den första delen av pipeline för repot:

   1. Ställ in inställningar för repot så att

      - Require a pull request before merging
      - Require approvals → “Required approving reviews: 1”
      - Dismiss stale approvals when new commits are pushed
      - Require status checks to pass → "lint"
      - Restrict who can push → lämna tomt (ingen ska få force‑pusha)
      - Require linear history (rebase skall göras, inte merge-commits)
      - granska och eventuellt justera reglerna i [pyproject.toml](../pyproject.toml) som kollas av verktyget [ruff](https://docs.astral.sh/ruff/tutorial/).

   1. Skapa ett job i [workflow](../.github/workflows/code_quality.yml) som heter "lint" och

      - kör lint på koden vid skapande av pull request
      - kör lint på koden vid push till main branch

1. Implementera de två routerna i koden som markerats med `TODO:`

   - `/api/v1/health` returnerar `{ "status": "ok" }`
   - `/status` returnerar en webbsida som innehåller repots commit-hash (eller `uncommitted changes`)

## Krav

Notera att under denna sprint behöver ni inte skriva testkod.

All kod som pushas till main branch MÅSTE:

- Gå igenom ci-workflow utan fel
- Ske genom pull request (PR) och tillhörande kodgranskning
- PR-skaparen ska följa mallen ([PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md))
- PR-granskaren ska använda kodgranskningschecklistan ([code_review_checklist.md](./checklists/code_review_checklist.md))
- PR skall vara godkänd av minst en person
- PR ska pushas <24h efter skapande, annars rebasa och skapa ny PR
- Stoppas av pipeline om inte ovan uppfylls
