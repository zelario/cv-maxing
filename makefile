.PHONY: run dev

dev:
	uvicorn src.api:app --reload

run: dev