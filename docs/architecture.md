# Architecture

This repository follows a layered structure designed to keep domain logic, synthetic data, service logic, and the HTTP layer separate.

## Layers

- `backend/src/sentinel/config.py` provides typed environment configuration.
- `backend/src/sentinel/domain.py` defines the domain objects used by the app.
- `backend/src/sentinel/data/synthetic.py` creates reproducible synthetic data with time-based splitting.
- `backend/src/sentinel/service.py` holds the business logic used by the API.
- `backend/src/sentinel/api.py` exposes the HTTP endpoints consumed by the frontend.
- `backend/src/sentinel/llm.py` validates provider configuration and invokes the fake, Anthropic,
  or Ollama adapter for analysis requests.
- `frontend/src/api.ts` is the shared typed API client.
- `frontend/src/hooks/` owns TanStack Query server state.
- `frontend/src/features/` separates case review, overview, and evaluation-result screens.
- `frontend/src/components/` contains shared navigation, status, metric, and query-state UI.

The Vite development server proxies `/api` requests to the local FastAPI service. Feature
screens receive data through hooks and pass it to presentational components, keeping
network state out of the UI primitives. The frontend implements an overview, searchable/filterable case queue with case details,
results, LLM analysis, editable memo submission, and provider settings. Anthropic API keys are
kept in frontend memory and passed only in analysis requests; local Ollama uses a configured
backend URL. The default fake provider is a placeholder. This local demo flow is not a
production secret-management setup or a full analyst production console.
