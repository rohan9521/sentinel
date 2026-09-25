# Decisions

## ADR-001: Synthetic-first project setup

We begin with synthetic data and an offline LLM so the project can run without external dependencies and still demonstrate the end-to-end workflow.

## ADR-002: Demo backend API first

The repository includes a lightweight FastAPI app up front because the front-end and evaluation layers depend on stable route contracts from the beginning.

## ADR-003: Offline demo readiness

The default provider is intentionally set to `fake` so the app can be used without a real API key while still providing a realistic contract for later integrations.

## ADR-004: Deterministic baseline evaluation

We added a seeded surrogate GBM baseline and a reproducible evaluation runner. Results are written to `results/baseline_demo.json` so all reported metrics are traceable to generated artifacts instead of hand-written numbers.

## ADR-005: Per-request model provider selection

The UI supports a no-call fake provider, Anthropic via a user-entered API key, and local Ollama.
The key is held only in frontend memory and sent to the backend for the individual request;
the backend does not persist it. Ollama uses a backend-configured local URL. This is intended
for local development, not as production secret management or a security boundary.
