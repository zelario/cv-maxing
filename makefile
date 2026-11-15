.PHONY: build app dev stop test cli

build:
	docker compose build

app:
	docker compose run --rm --service-ports web

dev:
	docker compose up -d dev

stop:
	docker compose stop dev && docker compose rm -f dev

test:
	@read -p "Test ID: " id && docker compose exec dev python tests/src/validation_pipeline.py --test-id $$id

cli:
	docker compose exec dev python src/cli.py
