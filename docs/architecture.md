# Architecture

This repository follows a layered structure designed to keep domain logic, synthetic data, service logic, and the HTTP layer separate.

## Layers

- `backend/src/sentinel/config.py` provides typed environment configuration.
- `backend/src/sentinel/domain.py` defines the domain objects used by the app.
- `backend/src/sentinel/data/synthetic.py` creates reproducible synthetic data with time-based splitting.
- `backend/src/sentinel/service.py` holds the business logic used by the API.
- `backend/src/sentinel/api.py` exposes the HTTP endpoints consumed by the frontend.
- `frontend/src/hooks/useCaseQueue.ts` provides a typed client-side fetch contract for the queue.

This keeps the application ready for later expansion into the model comparisons, agent tool layer, and evaluation pipeline described in the issue.
