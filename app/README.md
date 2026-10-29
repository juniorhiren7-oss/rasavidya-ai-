# API notes

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
cp .env.example .env
# Set ADMIN_API_TOKEN to a long random value before exposing the API.
uvicorn app.main:app --reload
```

Open API docs at `http://localhost:8000/docs`.

Endpoints:
- `GET /health` — health probe
- `GET /agents` — ten agent-role definitions
- `GET/POST /sources` — source metadata; POST requires `X-Admin-Token`
- `GET/POST /claims` — historical claim records; POST requires `X-Admin-Token`
- `GET/POST /assessments` — eight evidence dimensions; POST requires `X-Admin-Token`
- `GET /runs` — research-run history; requires `X-Admin-Token`
- `POST /runs` — synchronous model-assisted research; requires `X-Admin-Token` and `OPENAI_API_KEY`

All write and AI-run endpoints fail closed when `ADMIN_API_TOKEN` is unset. Send the token in the `X-Admin-Token` header. Store secrets only in the deployment environment, never in source control. Use HTTPS, rate limiting, and managed secret storage in production.
