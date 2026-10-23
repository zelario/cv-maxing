.PHONY: run dev test help docker-build docker-run docker-up docker-down

run: dev

dev:
	uvicorn src.api:app --reload

test:
	python tests/src/validation_pipeline.py

docker-build:
	docker compose build

docker-run:
	docker compose run --rm --service-ports cv-maxing

docker-up:
	docker compose up

docker-down:
	docker compose down
