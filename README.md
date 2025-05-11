# DevOps1 bloggapp

En enkel blogg-app byggd med FastAPI och Pydantic. Här får du öva på att bygga en CI-pipeline, skriva TDD-tester, köra integrationstester och deploya till AWS.

## Sprint-översikt

Appen kommer att växa över tid. Med varje ny sprint kan det komma nya filer och funktioner.

Läs mer om målen och kraven för varje sprint:

- [Sprint 1: Pull Requests, Lintning & Code Review](docs/sprint1.md)

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
├── .github/                  PR-mall & CI-workflows
├── app/                      Applikationskod (FastAPI)
├── docs/                     Sprintmål och instruktioner
├── infra/                    (kommer senare) Terraform-infrastruktur
├── tests/                    (kommer senare) Unit, integration & system
├── Dockerfile                För körning med Docker
├── Makefile                  Samling av kommandon för utveckling
├── requirements.in           beroenden för produktion
├── requirements-dev.in       beroenden för utveckling/pipeline
├── requirements.txt          Exakta beroenden för produktion (genererad från .in-filen)
├── requirements-dev.txt      Exakta beroenden för utveckling/pipeline (genererad från .in-filen)
├── pyproject.toml            Lint-konfiguration (Ruff)
└── README.md                 Denna fil
```

Filerna `requirements*.*` behöver ni antagligen inte röra men bra att veta vad de används till.
