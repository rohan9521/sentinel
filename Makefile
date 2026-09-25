# Makefile
PYTHON ?= python3
UV ?= uv

.PHONY: setup test check api web dev data train eval report docker-up backend-test frontend-test backend-check frontend-check

setup:
	cd backend && $(UV) sync --locked --all-extras
	cd frontend && npm ci

backend-test:
	cd backend && $(UV) run pytest

frontend-test:
	cd frontend && npm run test -- --run

test: backend-test frontend-test

backend-check:
	cd backend && $(UV) run ruff check . && $(UV) run ruff format --check . && $(UV) run mypy src tests

frontend-check:
	cd frontend && npm run lint && npm run typecheck && npm run test -- --run

check: backend-check frontend-check

api:
	cd backend && $(UV) run uvicorn sentinel.api:app --reload --host 0.0.0.0 --port 8000

web:
	cd frontend && npm run dev -- --host 0.0.0.0 --port 5173

dev:
	(cd backend && $(UV) run uvicorn sentinel.api:app --host 0.0.0.0 --port 8000) & \
	(cd frontend && npm run dev -- --host 0.0.0.0 --port 5173) & \
	wait

data:
	cd backend && $(UV) run python -m sentinel.cli generate-data

train:
	cd backend && $(UV) run python -m sentinel.cli train

eval:
	cd backend && $(UV) run python -m sentinel.cli eval

report:
	cd backend && $(UV) run python -m sentinel.cli report

docker-up:
	docker compose up --build
