import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_registry_has_ten_distinct_agents(client):
    response = client.get("/agents")
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 10
    assert len({agent["id"] for agent in payload["agents"]}) == 10


def test_source_starts_unverified(client):
    response = client.post("/sources", json={
        "title": "Test manuscript catalogue record",
        "authors": "Test editor",
        "publication_year": "1976",
        "source_type": "catalogue_record",
        "url": "https://example.org/catalogue",
        "notes": "Test-only record; no claim is verified.",
    })
    assert response.status_code == 201
    assert response.json()["verification_status"] == "user_added_unverified"


def test_invalid_agent_is_rejected(client):
    response = client.post("/runs", json={
        "agent_id": "arbitrary-sql-agent",
        "task": "Review source provenance and identify gaps.",
    })
    assert response.status_code == 422


def test_transmutation_requires_separate_nuclear_evidence():
    from app.evidence import meets_transmutation_evidence_gate

    base = {
        "source_authenticity": "strong",
        "translation_reliability": "strong",
        "historical_context": "supported",
        "chemical_plausibility": "supported",
        "analytical_quality": "strong",
        "independent_replication": "strong",
        "contamination_exclusion": "strong",
        "nuclear_origin_evidence": "strong",
    }
    assert meets_transmutation_evidence_gate(base)
    assert not meets_transmutation_evidence_gate({**base, "nuclear_origin_evidence": "partial"})
