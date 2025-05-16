# DevOps1 bloggapp

En enkel blogg-app byggd med FastAPI och Pydantic. Här får du öva på att bygga en CI-pipeline, skriva TDD-tester, köra integrationstester och deploya till AWS.

## Sprint-översikt

Appen kommer att växa över tid. Med varje ny sprint kan det komma nya filer och funktioner.

Läs mer om målen och kraven för varje sprint:

- [Sprint 1: Pull Requests, Lintning & Code Review](docs/sprint1.md)
- [Sprint 2: Enhetstester och testtäckning](docs/sprint2.md)

### Nyheter i appen och koden för sprint 2

Appen fungerar nu som en enklare blogg där man kan:

- `/`: Visa alla blogginlägg på startsidan
  - Klicka in på ett specifikt inlägg via sin titel (`/posts/{id}`)
- `/admin`: man kan skapa eller ta bort inlägg (kräver lösenord)

Data lagras för tillfället i en in-memory mockdatabas, vilket gör det enkelt att komma igång utan riktig databas (som kommer senare).

#### Testning och testtäckning

- Enhetstestning har förberetts:
  - [pytest-cov](https://pytest-cov.readthedocs.io/) har lagts till som utvecklingsberoende
- Code coverage rapportering i HTML-format är konfigurerad i [pyproject.toml](.pyproject.toml)
  - [ddb.py](./app/storage/ddb.py) och [start.py](./app/start.py) exkluderas eftersom den koden inte behöver testas

#### Ny CI-pipeline (påbörjad)

- Ny GitHub Actions-fil [.github/workflows/test.yml](.github/workflows/test.yml):
  - Innehåller `TODO`-sektioner för checkout, test, coverage och artefaktuppladdning

#### Förbättrad utvecklingsmiljö

- Makefile uppdaterad:
  - `python -m` används nu vilket gör det mer kompatibelt med virtualenv
- [.gitignore](.gitignore) utökad med `.venv`, coverage-filer och rapporter

#### Miljöhantering och feature flags

- Ny fil: [app/env.py](.app/env.py)
  - Läser `.env`-fil (om den finns)
  - Hanterar feature flags: `FEATURE_DDB`, `FEATURE_ADMIN`
  - Hämtar `ADMIN_PASSWORD`
- Ny [.env.example](.env.example) för att visa hur lokal miljö kan konfigureras

#### Datamodeller och mock-DDB

- Ny fil: [app/models.py](./app/models.py) med Pydantic-modeller för att validera data från databasen
- Ny mockdatabas: [app/storage/ddb.py](./app/storage/ddb.py) (in-memory med två inlägg)
  - Stöder `list_posts`, `get_post`, `create_post`, `delete_post`
  - Funktionalitet styrs med `FEATURE_DDB`

#### Appstruktur och routers

- [app/main.py](./app/main.py) omstrukturerad:
  - Separata funktioner för att mounta statiska filer, registrera routers, serva /robots.txt
- Ny [app/start.py](./app/start.py) används för Uvicorn start
- [app/routers/web.py](./app/routers/web.py) kraftigt utbyggd:
  - Stöder visning av posts, enskild post och adminpanel
  - CRUD-funktionalitet för inlägg via formulär
  - Behörighet styrs via `FEATURE_ADMIN` och lösenord (`ADMIN_PASSWORD`)

#### HTML

- [index.html](./app/templates/index.html) visar inlägg eller fallback-meddelande
- [post.html](./app/templates/post.html) visar ett specifikt inlägg
- [admin.html](./app/templates/admin.html) innehåller formulär för skapande/radering av inlägg (kräver lösenord: `ADMIN_PASSWORD`)

## Kom igång

### Förutsättningar

- Python 3.12
- Make
  - [Windows](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows)
  - [MacOs](https://stackoverflow.com/questions/10265742/how-to-install-make-and-gcc-on-a-mac)
  - [Linux](https://linuxhandbook.com/using-make/)
- (Valfritt) [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Installera och starta appen

1. Klona repot:

   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. Skapa virtuell miljö och installera beroenden:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   make install # installerar python-paketen som behövs för utveckling
   ```

3. Kör utvecklingsservern:

   ```bash
   make dev
   ```

   Öppna webbläsaren på [http://localhost:8000](http://localhost:8000).

### Andra kommandon

- `make lint`: kontrollerar lintern (kodformattering och lintregler)
- `make lint-fix`: fixar lintproblem (kodformattering och lintregler)
- `make test`: kör alla tester
- `make docker-run`: bygger image och startar appen i container ([http://localhost:8000](http://localhost:8000))

## Projektstruktur

```
.
├── .github/                  PR-mall & workflows
├── app/                      Applikationskod (FastAPI)
│   ├── env.py                Exponerar miljövariabler och feature flags
│   ├── main.py               Skapar app-instans, mountar statiska filer och routers
│   ├── models.py             Pydantic-modeller för blogginlägg
│   ├── routers/              API- och webb-routes
│   │   ├── api.py            Endpoints för API (ex. /api/v1/health)
│   │   └── web.py            Webbgränssnitt, HTML och formulär
│   ├── start.py              Startpunkt för appen (med hjälp av Uvicorn)
│   ├── static/
│   │   └── robots.txt        Förhindrar att appen indexeras av sökmotorer
│   ├── storage/              Databaslager (mock i Sprint 2)
│   │   └── ddb.py            In-memory databas med CRUD-metoder
│   └── templates/            HTML-mallar för renderade sidor
│       ├── admin.html        Adminpanel för att skapa och radera inlägg
│       ├── index.html        Startsida med lista över inlägg
│       ├── post.html         Visar ett enskilt inlägg
│       └── status.html       Statussida med commit-hash
├── docs/                     Sprintmål och instruktioner
├── infra/                    (kommer senare) Terraform-infrastruktur
├── tests/
│   ├── integration/
│   ├── system/
│   └── unit/                 Enhetstester
│       └── test_import.py    Ser till att moduler räknas med i coverage
├── Dockerfile                För körning med Docker
├── Makefile                  Samling av kommandon för utveckling
├── requirements.in           Beroenden för produktion
├── requirements-dev.in       Beroenden för utveckling/pipeline
├── requirements.txt          Exakta beroenden för produktion (genererad från .in-filen)
├── requirements-dev.txt      Exakta beroenden för utveckling/pipeline (genererad från .in-filen)
├── pyproject.toml            Lint- och testkonfiguration (Ruff, pytest-cov)
└── README.md                 Denna fil
```

Filerna `requirements*.*` behöver ni antagligen inte röra men bra att veta vad de används till.
