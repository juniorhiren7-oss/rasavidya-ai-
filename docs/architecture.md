# RASAVIDYA AI architecture

## System boundaries

- **Floot frontend:** research dashboard, sign-in UI, source browser, claim explorer, notebook and agent-run interface. Its current database and API are still hosted inside Floot.
- **GitHub backend:** this repository contains a separate FastAPI service, SQLAlchemy data models, optional model-assisted research endpoint, tests and container configuration. It is not yet deployed or wired to the Floot frontend.
- **PostgreSQL:** relational system of record for source metadata, historical claims, multidimensional evidence assessments and research-run history.
- **Vector retrieval (planned):** chunked, source-linked passages with stable document/page/verse anchors. Do not enable semantic answers without citations back to stored chunks.
- **OCR pipeline (planned):** source acquisition, page images, OCR/transcription candidates, confidence and human correction. Preserve source image and raw OCR; never overwrite a witness with a normalized guess.
- **Agent orchestration (MVP registry):** ten bounded roles are defined. They are role prompts, not ten autonomous workers running continuously. Each task must record the chosen role, input, status, output and errors.
- **Evidence graph (planned):** claims, source passages, interpretations, procedures, materials, experiments, observations and contradictions linked with provenance.

## Data flow

1. A researcher registers a source lead; the record starts unverified.
2. A future ingestion job captures permitted source content and bibliographic provenance.
3. OCR/transcription stores raw output, alternative readings and reviewer decisions separately.
4. A claim record points to a precise source/page/verse location. Verse 363 and verse 404 are separate records.
5. Historical interpretation is classified as alloying, amalgamation, gilding, compound formation, purification/concentration or claimed elemental transmutation.
6. Evidence dimensions are assessed independently; there is no single confidence score that hides missing nuclear evidence.
7. An authorized research run is saved with its agent ID, task, status, output and timestamps.
8. Reports show sources, uncertainty, contradictions and the next falsifiable test.

## Evidence dimensions

- source authenticity
- translation reliability
- historical context
- chemical plausibility
- analytical quality
- independent replication
- contamination exclusion
- nuclear-origin evidence

The transmutation gate is a minimum review checklist, not a declaration that transmutation occurred.

## Research benchmark

Start with the 1976 Rasārṇavakalpa edition catalogue lead and independently verify verse 363. Then review verse 404 as a separate passage. Do not merge passages into a recipe or assert exact Sanskrit wording until the printed witness has been inspected. Compare the relevant scholarly discussion by Vijaya Deshpande. Track the Rasārṇava 12.51 reconstruction as a separate secondary lead.

## Security boundaries

- Backend write operations and model-run endpoints require the X-Admin-Token header.
- The server fails closed if ADMIN_API_TOKEN is missing.
- Keep the admin token and provider key in deployment secret storage only.
- Add user-level identity, role-based authorization, request rate limits, audit logs and HTTPS before multi-user production.
- The Floot frontend's existing login does not automatically authenticate requests to this independent API.
- Do not expose the backend admin token in browser JavaScript. Use a trusted server-side proxy or authenticated backend session when connecting the frontend.

## Current versus planned

Implemented: FastAPI API, SQLAlchemy tables, ten agent definitions, optional model execution, admin-token gate, source/claim/assessment/run endpoints, starter seed data, Docker/Compose, GitHub Actions tests.

Planned: Alembic migrations, robust user authentication, source document storage, OCR queue/workers, vector index, evidence graph traversal, source citations from retrieved chunks, async job queue, integration contract with Floot, and end-to-end tests against a deployed environment.
