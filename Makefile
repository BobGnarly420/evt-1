.PHONY: install test lint run migrate seed docker
install:
	pip install -e .[dev]

test:
	pytest -q

lint:
	ruff check .

run:
	uvicorn app.main:app --reload

migrate:
	python scripts/migrate.py

seed:
	python scripts/seed.py

docker:
	docker compose up --build
