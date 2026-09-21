# Architecture

This repository follows the layered pattern described in the issue: domain logic stays pure, data generation remains separate, the API is thin, and the front-end consumes the backend through typed interfaces.

## Layering intent

- `backend/src/sentinel/config.py` holds typed environment settings.
- `backend/src/sentinel/domain.py` defines the core data models.
- `backend/src/sentinel/data/synthetic.py` generates synthetic, time-ordered data.
- `backend/src/sentinel/api.py` exposes a basic demo API.
- `frontend/src/App.tsx` renders the analyst-facing experience in offline mode.

The design ensures future agents, evaluation scripts, and richer UI features can be added without coupling each layer to the others.
