# docs/architecture.md
# Architecture

This repository uses a monotonic, layered structure intended to preserve separation between pure domain logic and infrastructure concerns.

## Layering intent

- `backend/src/sentinel`: core application code.
- `backend/tests`: tests for domain logic, synthetic data, and future LLM tooling.
- `frontend/src`: feature-oriented React UI code.

The architecture is intentionally lightweight in this initial setup but follows the eventual project direction: domain-first logic, injectable infrastructure, and reproducible evaluation artifacts in `results/`.

## Dependency direction

The domain layer should not import the API, database, or frontend concerns. Future modules should depend inward, never outward.

