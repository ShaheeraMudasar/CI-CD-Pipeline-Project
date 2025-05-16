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

# bygger och kör appen som Docker-container
docker-run:
	docker build -t blog-app .
	docker run --rm -p 8000:8000 blog-app