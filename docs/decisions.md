# docs/decisions.md
# Decisions

## ADR-001: Monorepo scaffold

We choose a monorepo with explicit `backend/`, `frontend/`, and `docs/` directories to make cross-language CI and evaluation simpler.

## ADR-002: Seeded randomness and fake LLM defaults

All randomness is constrained by environment-based settings and a default fake LLM provider so the repo can run offline and without external credentials.

## ADR-003: Synthetic data first

The initial implementation begins with a synthetic generator and time-based split tests so we can validate the workflow before introducing heavier modeling or evaluation code.

