# Decisions

## ADR-001: Synthetic-first project setup

We begin with synthetic data and an offline LLM so the project can run without external dependencies and still demonstrate the end-to-end workflow.

## ADR-002: Demo backend API first

The repository includes a lightweight FastAPI app up front because the front-end and evaluation layers depend on stable route contracts from the beginning.

## ADR-003: Offline demo readiness

The default provider is intentionally set to `fake` so the app can be used without a real API key while still providing a realistic contract for later integrations.
