[![codecov](https://codecov.io/github/ShaheeraMudasar/CI-CD-Pipeline-Project/graph/badge.svg?token=4EMVYZ81DU)](https://codecov.io/github/ShaheeraMudasar/CI-CD-Pipeline-Project)

## FastAPI Blog App — CI/CD DevOps Pipeline Project

This project showcases a production-grade CI/CD pipeline for a FastAPI-based blog application. The pipeline automates code quality checks, testing (unit and integration), and cloud deployment to AWS using modern DevOps tools and best practices.

---

👥 **Team Collaboration Note**

This was a group project built during a DevOps course. All members collaborated closely across the full development lifecycle — from test automation to infrastructure provisioning and deployment. We followed DevOps principles like automation, quality assurance, and continuous improvement throughout the project.

---

🔍 **Project Overview**

We were given an initial FastAPI application and tasked with integrating it into a robust DevOps workflow. The project implements:

- Automated linting, unit testing, and integration testing in CI
- 75% minimum test coverage enforcement
- Environment-specific logic for local and cloud behavior
- Infrastructure-as-Code with Terraform (OpenTofu)
- Continuous deployment to AWS with rollback-safe practices
- Secure secret management via GitHub Actions

---

🧪 **Testing & Quality Assurance**

The project enforces code quality and correctness at every stage of the pipeline:

### ✅ Linting

- Uses `ruff` for linting and static code analysis
- Automatically triggered via GitHub Actions on pull requests and main branch pushes

### ✅ Unit Testing

- Located in `tests/unit/`
- Written using `pytest` and `pyhamcrest`
- Enforces a **minimum 75% coverage** threshold (defined in `pyproject.toml`)
- Merges are blocked if coverage falls below threshold
- Coverage is displayed in CI logs for visibility

### ✅ Integration Testing

- Located in `tests/integration/`
- Uses `FastAPI TestClient` against a local DynamoDB instance (mocked via Localstack)
- Local setup and test execution managed with `Makefile` commands
- Integration tests run as a separate CI job, independently from unit tests

### ✅ End-to-End (System) Testing

- Located in `tests/system/`
- Executed automatically after deployment to AWS
- Validates that the live application functions correctly

---

🚀 **CI/CD Pipeline**

Automated workflows are managed using **GitHub Actions** and configured to ensure high code quality and safe delivery.

### Workflows

- `code_quality.yml`: Runs `ruff` on pull requests and main branch
- `test.yml`: Executes unit tests and enforces coverage
- `integ_test.yml`: Runs integration tests with Localstack
- `deploy-to-dev.yml`: Deploys app to AWS dev environment when `DEPLOY_ENABLED=true`
- `destroy-infrastructure.yml`: Manually triggered workflow to tear down infrastructure

### Branch Protection

- Pull requests are required for merging
- Status checks (lint, unit test, integration test) must pass
- Linear commit history (rebase required)
- No force-pushes allowed

---

🛠️ **Tools & Technologies Used**

- **FastAPI**, **Pydantic** – Application framework
- **pytest**, **pytest-cov**, **pyhamcrest** – Testing & coverage
- **Ruff** – Linting
- **Localstack** – Local AWS service simulation
- **Docker**, **Docker Compose** – Local dev and test environment
- **Terraform (OpenTofu)** – Infrastructure provisioning
- **GitHub Actions** – CI/CD orchestration
- **AWS** – AppRunner, DynamoDB, ECR
- **Makefile** – Local development automation

---
## Project Structure

```
.
├── .github/                  # PR templates & workflows
│   └── workflows/            # GitHub Actions workflows
│       ├── code_quality.yml              Code linting and quality checks
│       ├── deploy-to-dev.yml             Creates dev infrastructure and deploys the app
│       ├── destroy-infrastructure.yml    Removes all infrastructure (triggered manually)
│       ├── integ_test.yml                Integration tests
│       └── test.yml                      Unit tests
├── app/                      # Application code (FastAPI)
│   ├── env.py                Environment variables and feature flags
│   ├── main.py               Creates app instance, mounts static files and routers
│   ├── models.py             Pydantic models for blog posts
│   ├── routers/              API and web routes
│   │   ├── api.py            API endpoints (e.g. /api/v1/health)
│   │   └── web.py            Web interface, HTML, and forms
│   ├── start.py              Entrypoint for the app (via Uvicorn)
│   ├── static/
│   │   └── robots.txt        Prevents search engine indexing
│   ├── storage/              Database layer with environment-aware credential handling
│   │   ├── ddb.py            DynamoDB interaction code (local and prod)
│   │   └── ddb_mock.py       In-memory DB with CRUD methods
│   └── templates/            HTML templates for rendered pages
│       ├── admin.html        Admin panel for creating/deleting posts
│       ├── index.html        Homepage with list of posts
│       ├── post.html         Displays a single post
│       └── status.html       Status page with commit hash
├── docs/                     Sprint goals and instructions
├── infra/                    Infrastructure as Code (Terraform/OpenTofu)
│   ├── backend.tf            Terraform backend config
│   ├── variables.tf          Input variables for infra
│   ├── apprunner.tf          AWS AppRunner service and ECR repo
│   ├── dynamodb.tf           DynamoDB table for production
│   ├── outputs.tf            Infrastructure outputs
│   ├── create-tfstate-backend.sh  Script to init remote backend (safe to run multiple times)
│   ├── create-ecr.sh         Script to create ECR repo (idempotent)
│   └── local/
│       └── init.py           Initializes DynamoDB table in Localstack
├── tests/
│   ├── integration/          Integration tests
│   │   └── test_localstack_and_ddb_table.py     Verifies Localstack and config
│   ├── system/               End-to-end tests for deployed app
│   └── unit/                 Unit tests
│       └── test_import.py    Ensures modules are included in coverage
├── Dockerfile                For running app in Docker
├── docker-compose.yml        For running Localstack (via Docker)
├── Makefile                  Collection of local dev commands
├── requirements.in           Production dependencies
├── requirements-dev.in       Dev/pipeline dependencies
├── requirements.txt          Exact production dependencies (generated)
├── requirements-dev.txt      Exact dev/pipeline dependencies (generated)
├── pyproject.toml            Lint/test config (Ruff, pytest-cov)
└── README.md                 This file
```


---

🔐 **Secrets & Configuration**

GitHub Actions secrets and variables are used to securely manage infrastructure and deployment:

| Name                    | Type    | Description                          |
|-------------------------|---------|--------------------------------------|
| `DEPLOY_ENABLED`        | Variable | Toggle for enabling deployment       |
| `AWS_ACCOUNT_ID`        | Variable | AWS account ID                       |
| `AWS_ACCESS_KEY_ID`     | Secret   | AWS IAM access key                   |
| `AWS_SECRET_ACCESS_KEY` | Secret   | AWS IAM secret key                   |
| Additional TF variables | Variable | Defined in `infra/variables.tf`      |

These are configured under **Settings → Secrets and variables → Actions** in the GitHub repository.

---

---

📄 **Environment Configuration**

All environment variables used for local development are defined in the included `.env.example` file.

To set up your local environment, copy the file:

```bash
cp .env.example .env
```

This file includes feature flags, admin credentials for testing, and mock AWS settings for Localstack. These values are **not sensitive** and are only meant to demonstrate how the application works in a local or demo environment.

> ⚠️ **Security Note:**  
> The `.env.example` file contains hardcoded credentials like `ADMIN_PASSWORD`, which are intentionally included to support demo/testing workflows. In real-world deployments, such values should never be committed to version control and should instead be handled using GitHub Secrets, environment variables, or secret managers.

💻 **Running the Project Locally**

```bash
# Clone the repo
git clone https://github.com/ShaheeraMudasar/CI-CD-Pipeline-Project.git
cd CI-CD-Pipeline-Project

# Set up a Python virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run lint checks
make lint

# Run unit tests
make test

# Start Localstack and initialize local DynamoDB
make localstack-up

# Run integration tests
make test-integ

# Run the app 
make dev
```

---

🚧 **Known Limitations**

- `DEPLOY_ENABLED` is set to `false` by default to avoid accidental deployments during development
- The pipeline currently targets only a shared **development** environment — no staging or production setup is in place
- Deployment requires manual configuration of AWS secrets and enabling flags
- End-to-end (system) tests run only in the cloud environment after deployment, and are not mocked locally
- While infrastructure provisioning is automated, full rollback mechanisms or failure recovery steps are not implemented
