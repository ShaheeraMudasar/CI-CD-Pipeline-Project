# inspiration: https://www.codementor.io/@adammertz/quick-tip-how-i-use-pip-tools-to-wrangle-dependencies-1fzreskhok

# installerar paket som behövs för utveckling
install:
	@pip install \
	-r requirements.txt \
	-r requirements-dev.txt

compile:
	@rm -f requirements*.txt
	@pip-compile requirements.in > requirements.txt
	@pip-compile requirements-dev.in > requirements-dev.txt
    
sync:
	@pip-sync requirements*.txt

# startar appen lokalt (utan docker)
dev:
	python -m uvicorn app.start:app --reload

dev-local: localstack-up
	python -m uvicorn app.start:app --reload

# startar localstack med en lokal AWS-miljö (i detta fall för DynamoDB)
# Om inte finns, skapar DynamoDB tabellen som behövs för att kunna använda den lokala AWS-miljön
localstack-up:
	docker compose up -d localstack
	python -m infra.local.init

# kontrollerar kodstil och linter-regler
lint:
	@echo "→ Kör Ruff format-check (utan autoformatering)..."
	-python -m ruff format --check .
	@echo "→ Kör Ruff lint-check (utan auto-fix)..."
	-python -m ruff check .
	
# automatisk fix av formattering och enklare linter-problem
lint-fix:
	@echo "→ Kör Ruff autoformat och auto-fix..."
	python -m ruff format .
	python -m ruff check . --fix

# kör alla test
# `python -m` är så att det ska funka med virtual env
test:
	python -m pytest 

# kör unit test
# `python -m` är så att det ska funka med virtual env
test-unit:
	python -m pytest tests/unit

# kör integrationstest
# vid körning av endast integrationstest behöver inte coverage-nås
# `python -m` är så att det ska funka med virtual env
test-integ: localstack-up
	python -m pytest --no-cov tests/integration

# bygger och kör appen som Docker-container
docker-run:
	docker build -t blog-app .
	docker run --rm -p 8000:8000 blog-app