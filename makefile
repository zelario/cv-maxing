.PHONY: build app dev stop

build:
	docker compose build

app:
	docker compose run --rm --service-ports web

dev:
	docker compose up -d dev

stop:
	docker compose stop dev && docker compose rm -f dev
