.PHONY: install dev dev-frontend dev-backend lint lint-frontend lint-backend test format

install:
	cd frontend && npm install
	cd backend && pip install -e ".[dev]"

dev:
	$(MAKE) dev-backend & $(MAKE) dev-frontend & wait

dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && uvicorn app.main:app --reload

lint: lint-frontend lint-backend

lint-frontend:
	cd frontend && npm run lint

lint-backend:
	cd backend && ruff check . && mypy app

format:
	cd frontend && npm run format
	cd backend && ruff format .

test:
	cd backend && pytest
