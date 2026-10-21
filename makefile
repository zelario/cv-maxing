.PHONY: build run run-d stop down logs ps test clean dev help

build:
	docker compose build

run:
	docker compose up

run-d:
	docker compose up -d

stop:
	docker compose stop

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

test:
	docker compose run --rm cv-maxing python tests/src/validation_pipeline.py

clean:
	docker compose down -v

dev:
	uvicorn src.api:app --reload
