# API notes

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
cp .env.example .env
uvicorn app.main:app --reload
```

Open API docs at `http://localhost:8000/docs`.

Endpoints:
- `GET /health` — health probe
- `GET /agents` — ten agent-role definitions
- `GET/POST /sources` — source metadata (new sources remain unverified)
- `GET/POST /claims` — historical claim records
- `GET/POST /assessments` — eight evidence dimensions
- `GET /runs` — research-run history
- `POST /runs` — synchronous model-assisted research; requires `OPENAI_API_KEY`

This initial API scaffold has no authentication layer yet. Do not expose write or model-run endpoints to the public internet until authentication, authorization, request rate limiting, and deployment secrets are configured. The Floot prototype independently restricts its own agent endpoints to administrators; that does not secure this API automatically.
