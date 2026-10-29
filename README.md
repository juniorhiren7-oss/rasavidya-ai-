# RASAVIDYA AI

Evidence-led research infrastructure for Rasashastra manuscripts, historical claims about metal transformation, modern materials science, and nuclear-evidence assessment.

## Current implementation

- FastAPI backend with health, agent registry, source, historical claim, evidence-assessment, and research-run endpoints.
- SQLAlchemy models compatible with local SQLite or PostgreSQL.
- Ten role-specific research agent definitions.
- Optional OpenAI Responses API execution, disabled until a key is configured.
- Admin-token protection for all writes and AI-run history/execution.
- Evidence gate that keeps source authenticity, translation, analytical quality, replication, contamination controls and nuclear-origin evidence distinct.
- Dockerfile, PostgreSQL Compose configuration, and GitHub Actions test workflow.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
cp .env.example .env
# Set a long random ADMIN_API_TOKEN in .env.
uvicorn app.main:app --reload
```

Browse `http://localhost:8000/docs`. The API defaults to SQLite; Docker Compose uses PostgreSQL.

## Tests

```bash
pip install -e ".[test]"
pytest
```

GitHub Actions runs the tests on pushes and pull requests to `main`.

## Research integrity and safety

- Keep primary-source wording separate from secondary interpretation and modern scientific explanation.
- Preserve page/verse references and uncertain OCR; never fabricate missing text.
- Distinguish alloying, amalgamation, gilding, compounds, purification, and claimed elemental transmutation.
- A gold-like appearance does not prove elemental gold; ordinary chemistry does not change atomic number.
- Nuclear-transmutation claims require defensible composition/isotope evidence, contamination controls, and independent replication.
- Do not publish executable hazardous procedures involving mercury, arsenic, toxic reagents, or radiation.

## Important deployment status

This repository is separate from the Floot frontend. The API is not yet deployed or connected to Floot. Configure `ADMIN_API_TOKEN`, an AI-provider key if needed, HTTPS, rate limiting, and secret storage before public deployment. The initial repository is public; keep all real keys out of Git history.
