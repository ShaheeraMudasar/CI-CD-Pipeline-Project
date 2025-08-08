[![codecov](https://codecov.io/github/khdev-devops/dev24m_devops1_fast_commits/graph/badge.svg?token=HF2M4Q94AH)](https://codecov.io/github/khdev-devops/dev24m_devops1_fast_commits)

# DevOps1 bloggapp

En enkel blogg-app byggd med FastAPI och Pydantic. Här får du öva på att bygga en CI-pipeline, skriva TDD-tester, köra integrationstester och deploya till AWS.

## Sprint-översikt

Appen kommer att växa över tid. Med varje ny sprint kan det komma nya filer och funktioner.

Läs mer om målen och kraven för varje sprint:

- [Sprint 1: Pull Requests, Lintning & Code Review](docs/sprint1.md)
- [Sprint 2: Enhetstester och testtäckning](docs/sprint2.md)
- [Sprint 3: Integrationstester med hjälp av Localstack](docs/sprint3.md)
- [Sprint 4: Deployment & variabler](docs/sprint4.md)

### Sprint 4: Från Integration till Driftsättning (`Deploy to Dev`)

I de tidigare sprintarna har vi byggt en robust **CI-pipeline (Continuous Integration)**. Den har automatiskt verifierat att vår kod är korrekt formaterad, att enhetstester passerar och att integrationen med databasen fungerar som den ska. Målet har varit att tryggt kunna slå ihop (integrera) kod från flera utvecklare till vår `main`-branch.

Men en applikation som bara finns på GitHub är inte till mycket nytta. I Sprint 4 tar vi nästa logiska steg: **Continuous Delivery/Deployment**. Vi utökar vår pipeline så att den inte bara testar koden, utan också automatiskt paketerar och driftsätter den till en live-miljö i molnet. Detta är det sista, avgörande steget för att leverera värde till våra användare.

Vi gör detta i en säker, isolerad **`dev`-miljö**. Detta är teamets gemensamma sandlåda i AWS, en plats där vi kan se vår applikation fungera "på riktigt" för första gången, utan att riskera att påverka några slutanvändare.

#### AWS AppRunner: Motorn i vår infrastruktur

För att köra vår applikation i AWS använder vi en tjänst som heter **AWS AppRunner**. Man kan tänka på AppRunner som en "motor" för webbapplikationer. Istället för att vi själva måste hantera servrar, nätverk och operativsystem, säger vi bara till AppRunner: "Här är min applikation, se till att den körs och är tillgänglig på internet."

AppRunner är byggd för att köra **containeriserade applikationer**. Det är här Docker och ECR kommer in i bilden:

1.  **`Dockerfile`**: Detta är vår ritning som beskriver hur vår Python-applikation och alla dess beroenden ska paketeras till en standardiserad "låda" – en **Docker-image**. Denna image innehåller allt appen behöver för att köra, oavsett var den körs.
2.  **AWS ECR (Elastic Container Registry)**: Detta är vårt privata bibliotek i molnet där vi lagrar våra Docker-images. Man kan se det som ett "GitHub för Docker-images". Vår pipeline kommer att bygga en image och "pusha" upp den till ECR.
3.  **AWS AppRunner**: Slutligen instruerar vi AppRunner att hämta en specifik image från vårt ECR-bibliotek och köra den. AppRunner sköter sedan allt: den startar containern, ser till att den har tillräckligt med minne och CPU, och skapar en publik URL så att vi kan nå appen.

**Sammanfattning av flödet:**
`Dockerfile` → `Docker Image` → `AWS ECR` → `AWS AppRunner`

> **Läs mer:**
>
> - [AWS AppRunner, arkitektur och koncept (Officiell översikt)](https://docs.aws.amazon.com/apprunner/latest/dg/architecture.html)
> - [Vad är en Container? (Dockers förklaring)](https://www.docker.com/resources/what-container/)
> - [Vad är AWS ECR? (Officiell översikt)](https://aws.amazon.com/ecr/)

#### Säkerhet i vår Pipeline: Hur GitHub pratar med AWS (OIDC)

När vår pipeline behöver utföra uppgifter i AWS, som att driftsätta vår app, måste den kunna bevisa sin identitet på ett säkert sätt. Istället för att använda riskfyllda, permanenta lösenord använder vi en modern standard som heter **OpenID Connect (OIDC)**. Tänk på det som en digital passkontroll: istället för en statisk accessnyckel, får vår pipeline ett temporärt och unikt "pass" (en OIDC-token) från GitHub för varje enskild körning.

AWS är konfigurerat att lita på dessa "pass" från just ert GitHub-repository. När pipelinen visar upp sitt pass, svarar AWS genom att låta den "låna" en uppsättning tillfälliga behörigheter. Dessa behörigheter är definierade i en **IAM-roll** som jag redan har förberett åt er: `devops1-GitHubWorkflow`. Denna roll ger pipelinen precis de rättigheter den behöver för att driftsätta er app, och ingenting mer. Hela denna säkra handskakning sker automatiskt i bakgrunden.

I praktiken ser ni detta hända i `deploy-to-dev.yml`-filen i steget `Configure AWS credentials`. Genom att peka på den förberedda rollen kan vår pipeline interagera med AWS helt utan att vi någonsin behöver hantera eller lagra några hemliga nycklar i GitHub. Detta minimerar säkerhetsriskerna och är standardpraxis i moderna molnmiljöer.

Läs mer:

- [OpenID Connect (GitHubs dokumentation)](https://docs.github.com/en/actions/concepts/security/openid-connect)

#### Samarbete och Felsökning: `devops1-GroupViewer`-rollen

Eftersom ni som team endast driftsätter till **ett** av era AWS-konton, är det viktigt att alla i teamet kan se vad som händer, särskilt om något går fel. För att lösa detta har jag förberett en speciell roll som heter `devops1-GroupViewer`. Tänk på den som ett gästpass som ger er `read-only`-behörigheter till deployment-kontot. Med denna roll kan ni från era egna konton se AppRunner-tjänsten, kontrollera status på driftsättningar och, viktigast av allt, läsa loggarna i CloudWatch. Detta är avgörande för att ni ska kunna samarbeta effektivt vid felsökning.

När ni behöver titta på resurserna i det gemensamma deployment-kontot, loggar ni först in på ert **eget** AWS-konto. Därefter använder ni funktionen "Switch Role" i AWS-konsolen för att temporärt "låna" `devops1-GroupViewer`-rollens behörigheter i det andra kontot. Ni kommer att behöva ange **konto-ID:t** för det konto ni deployar till samt **rollnamnet**, vilket är `devops1-GroupViewer`.

**Guide:** [Så här byter du till en roll i AWS-konsolen (AWS Dokumentation)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html)

#### Vår `Deploy to Dev`-pipeline i detalj

Vårt nya workflow, `deploy-to-dev.yml`, orkestrerar hela denna process. Varje steg har ett tydligt syfte och bygger vidare på det föregående.

**Steg 1: Setup & Konfiguration**

- **Vad?** Pipelinen checkar ut koden och använder en säker OIDC-anslutning för att få temporära AWS-credentials.
- **Varför?** Detta är grunden. Vi behöver koden för att kunna bygga den, och vi behöver säkra, lösenordsfria rättigheter för att kunna interagera med AWS.

**Steg 2: Bootstrap – Förbered Spelplanen**

- **Vad?** Pipelinen kör två **idempotenta** bootstrap-skript. "Idempotent" betyder att de kan köras om och om igen utan att orsaka problem. Skripten säkerställer att den S3-bucket och den DynamoDB-tabell som OpenTofu behöver för att spara sitt tillstånd (`state`) existerar. De ser även till att vårt ECR-repository finns på plats.
- **Varför?** Genom att köra detta i början av varje deploy, garanterar vi att förutsättningarna för vår infrastruktur alltid är korrekta, även om det är den allra första körningen. Detta gör pipelinen självförsörjande och robust.

**Steg 3: Bygg Artefakten (Docker Image)**

- **Vad?** Pipelinen genererar en unik **image-tagg** från den aktuella comittens SHA-hash (t.ex. `a1b2c3d`). Sedan byggs en Docker-image enligt vår `Dockerfile` och pushas till ECR med denna unika tagg.
- **Varför?** Vi skapar en **oföränderlig (immutable) artefakt**. Varje version av vår kod får en unik, spårbar paketering. Detta är kritiskt för att kunna göra säkra och förutsägbara driftsättningar och, om nödvändigt, enkla rollbacks. Vi undviker den opålitliga `:latest`-taggen.

**Steg 4: Driftsätt Infrastruktur & Applikation (OpenTofu)**

- **Vad?** Pipelinen kör `tofu apply`. OpenTofu läser våra `.tf`-filer och jämför dem med det nuvarande tillståndet i AWS.
- **Varför?** Detta är hjärtat i IaC. Tofu ser att `image_tag`-variabeln har ett nytt värde. Den instruerar då AppRunner att starta en ny deployment-process och hämta den nya imagen från ECR. All annan infrastruktur, som DynamoDB-tabellen, lämnas orörd om den inte har ändrats i koden.

**Steg 5: Övervaka & Verifiera**

- **Vad?** Efter att `tofu apply` är klar, startar ett skript som aktivt frågar AppRunner om statusen på driftsättningen. När AppRunner rapporterar att den nya versionen är uppe, körs våra **End-to-End (E2E) tester** mot den publika URL:en.
- **Varför?** En lyckad `tofu apply` betyder bara att vi har bett AWS att göra något. Det betyder inte att applikationen faktiskt startade korrekt. Vi måste aktivt övervaka processen och sedan köra tester mot den live-miljön för att få ett slutgiltigt kvitto på att allt fungerar.

**Steg 6: Markera Framgång (Git Tag)**

- **Vad?** Endast om alla tidigare steg har lyckats, skapar pipelinen en ny Git-tagg (t.ex. `deploy-dev-a1b2c3d-20250801-1530`) och pushar den till repot.
- **Varför?** Detta skapar en permanent och lättläst historik över exakt vilka versioner av koden som har driftsatts till vår `dev`-miljö. Det gör det enkelt att se vad som är live och att referera till specifika releaser.

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

3. Kör utvecklingsservern (lokalt med localstack istället för riktig AWS DynDB):

   ```bash
   make dev-local
   ```

   Öppna webbläsaren på [http://localhost:8000](http://localhost:8000).

### Andra kommandon

- `make lint`: kontrollerar lintern (kodformattering och lintregler)
- `make lint-fix`: fixar lintproblem (kodformattering och lintregler)
- `make test`: kör alla tester
- `make docker-run`: bygger image och startar appen i container ([http://localhost:8000](http://localhost:8000))
- `make dev-local` : startar appen lokalt ihop med Localstack (körs i docker)
- `make localstack-up` : startar Localstack i Docker med en lokal AWS-miljö (vi använder den för DynamoDB)
- `make test-unit` : kör alla unit-test
- `make test-integ` : kör alla integrationstest
- `make test-system` : kör systemtest mot deployed miljö
- `make test-e2e` : kör end-to-end tester

## Lokal körning med Localstack

Localstack är ett verktyg som emulerar AWS-tjänster lokalt, så att du kan utveckla och testa applikationer utan att använda riktiga AWS-resurser. Du kan läsa mer om Localstack här: https://docs.localstack.cloud/getting-started/

Appen använder sig av AWS DynamoDB som databas. För att kunna köra lokalt använder vi Localstack (körs i Docker). Funktionaliteten styrs via miljövariabler och feature flags.

**OBS!** Localstack i detta projekt är konfigurerad utan volym i Docker. Det innebär att DynamoDB-tabeller och annan data inte sparas mellan uppstarter. Det är därför viktigt att localstack-up körs varje gång du startar Localstack, så att tabellen återskapas.

Se `dev-local` och `localstack-up` i [Makefile](Makefile) för att se hur Localstack startas och initieras.

## Projektstruktur

```
.
├── .github/                  PR-mall & workflows
│   └── workflows/            GitHub Actions workflows
│       ├── code_quality.yml              Kod-kvalitet checks
│       ├── deploy-to-dev.yml             Skapar dev infrastruktur och gör deployment av app
│       ├── destroy-infrastructure.yml    Tar bort all infrastruktur (triggas manuell)
│       ├── integ_test.yml                Integrationstester
│       └── test.yml                      Enhetstester
├── app/                      Applikationskod (FastAPI)
│   ├── env.py                Miljövariabler, feature flags och miljödetektering
│   ├── main.py               Skapar app-instans, mountar statiska filer och routers
│   ├── models.py             Pydantic-modeller för blogginlägg
│   ├── routers/              API- och webb-routes
│   │   ├── api.py            Endpoints för API (ex. /api/v1/health)
│   │   └── web.py            Webbgränssnitt, HTML och formulär
│   ├── start.py              Startpunkt för appen (med hjälp av Uvicorn)
│   ├── static/
│   │   └── robots.txt        Förhindrar att appen indexeras av sökmotorer
│   ├── storage/              Databaslager med miljömedveten credential-hantering
│   │   ├── ddb.py            Databaskod mot DynamoDB (lokal och produktion)
│   │   └── ddb_mock.py       In-memory databas med CRUD-metoder
│   └── templates/            HTML-mallar för renderade sidor
│       ├── admin.html        Adminpanel för att skapa och radera inlägg
│       ├── index.html        Startsida med lista över inlägg
│       ├── post.html         Visar ett enskilt inlägg
│       └── status.html       Statussida med commit-hash
├── docs/                     Sprintmål och instruktioner
├── infra/                    Infrastruktur som kod (Terraform/OpenTofu)
│   ├── backend.tf            Terraform backend-konfiguration
│   ├── variables.tf          Input-variabler för infrastruktur
│   ├── apprunner.tf          AWS AppRunner service och ECR repository
│   ├── dynamodb.tf           DynamoDB tabell för produktion
│   ├── outputs.tf            Infrastructure outputs
│   ├── create-tfstate-backend.sh  Script för backend-setup (idempotent, dvs säkert att köra flera gånger)
│   ├── create-ecr.sh         Script för ECR repository-skapande (idempotent, dvs säkert att köra flera gånger)
│   └── local/
│       └── init.py           Skapar/initierar DynamoDB tabell i Localstack
├── tests/
│   ├── integration/          Integrationstester
│   │   └── test_localstack_and_ddb_table.py     Test som kollar att Localstack och konfiguration är på plats
│   ├── system/               End-to-end tester mot deployed miljö
│   └── unit/                 Enhetstester
│       └── test_import.py    Ser till att moduler räknas med i coverage
├── Dockerfile                För körning med Docker
├── docker-compose.yml        För körning av Localstack (i Docker)
├── Makefile                  Samling av kommandon för utveckling
├── requirements.in           Beroenden för produktion
├── requirements-dev.in       Beroenden för utveckling/pipeline
├── requirements.txt          Exakta beroenden för produktion (genererad från .in-filen)
├── requirements-dev.txt      Exakta beroenden för utveckling/pipeline (genererad från .in-filen)
├── pyproject.toml            Lint- och testkonfiguration (Ruff, pytest-cov)
└── README.md                 Denna fil
```

Filerna `requirements*.*` behöver ni antagligen inte röra men bra att veta vad de används till.
