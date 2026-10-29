from datetime import datetime, timezone
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents import AGENTS, build_system_prompt, get_agent, list_agents
from app.config import get_settings
from app.database import get_db, init_db
from app.models import EvidenceAssessment, HistoricalClaim, ResearchRun, ResearchSource
from app.schemas import (
    ClaimCreate, ClaimRead, EvidenceAssessmentCreate, EvidenceAssessmentRead,
    ResearchRunRead, ResearchRunRequest, SourceCreate, SourceRead,
)

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Evidence-led research API for Rasashastra history, materials science and transmutation claims.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "rasavidya-ai-api", "version": app.version}


@app.get("/agents", tags=["agents"])
def agents() -> dict:
    return {"agents": list_agents(), "count": len(AGENTS)}


@app.get("/sources", response_model=list[SourceRead], tags=["research"])
def get_sources(limit: int = Query(default=100, ge=1, le=500), db: Session = Depends(get_db)):
    return list(db.scalars(select(ResearchSource).order_by(ResearchSource.created_at.desc()).limit(limit)))


@app.post("/sources", response_model=SourceRead, status_code=201, tags=["research"])
def create_source(payload: SourceCreate, db: Session = Depends(get_db)):
    source = ResearchSource(
        id=str(uuid4()), title=payload.title, authors=payload.authors,
        publication_year=payload.publication_year, source_type=payload.source_type,
        url=str(payload.url), notes=payload.notes, verification_status="user_added_unverified",
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@app.get("/claims", response_model=list[ClaimRead], tags=["research"])
def get_claims(limit: int = Query(default=100, ge=1, le=500), db: Session = Depends(get_db)):
    return list(db.scalars(select(HistoricalClaim).order_by(HistoricalClaim.created_at.desc()).limit(limit)))


@app.post("/claims", response_model=ClaimRead, status_code=201, tags=["research"])
def create_claim(payload: ClaimCreate, db: Session = Depends(get_db)):
    if db.get(HistoricalClaim, payload.id):
        raise HTTPException(status_code=409, detail="Claim ID already exists")
    if payload.source_id and not db.get(ResearchSource, payload.source_id):
        raise HTTPException(status_code=404, detail="Source not found")
    claim = HistoricalClaim(**payload.model_dump(), verification_status="unverified")
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


@app.get("/assessments", response_model=list[EvidenceAssessmentRead], tags=["evidence"])
def get_assessments(claim_id: str | None = None, db: Session = Depends(get_db)):
    statement = select(EvidenceAssessment).order_by(EvidenceAssessment.created_at.desc())
    if claim_id:
        statement = statement.where(EvidenceAssessment.claim_id == claim_id)
    return list(db.scalars(statement))


@app.post("/assessments", response_model=EvidenceAssessmentRead, status_code=201, tags=["evidence"])
def create_assessment(payload: EvidenceAssessmentCreate, db: Session = Depends(get_db)):
    if not db.get(HistoricalClaim, payload.claim_id):
        raise HTTPException(status_code=404, detail="Claim not found")
    if db.get(EvidenceAssessment, payload.id):
        raise HTTPException(status_code=409, detail="Assessment ID already exists")
    assessment = EvidenceAssessment(**payload.model_dump())
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment


@app.get("/runs", response_model=list[ResearchRunRead], tags=["agents"])
def get_runs(limit: int = Query(default=50, ge=1, le=200), db: Session = Depends(get_db)):
    return list(db.scalars(select(ResearchRun).order_by(ResearchRun.created_at.desc()).limit(limit)))


@app.post("/runs", response_model=ResearchRunRead, status_code=202, tags=["agents"])
def run_research(payload: ResearchRunRequest, db: Session = Depends(get_db)):
    agent = get_agent(payload.agent_id)
    if not agent:
        raise HTTPException(status_code=422, detail="Unknown research agent ID")
    if len(payload.task) > settings.max_research_task_chars:
        raise HTTPException(status_code=422, detail="Research task exceeds configured size limit")
    if payload.claim_id and not db.get(HistoricalClaim, payload.claim_id):
        raise HTTPException(status_code=404, detail="Claim not found")
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="AI provider is not configured. Set OPENAI_API_KEY in the backend environment before running agents.",
        )
    run = ResearchRun(
        id=str(uuid4()), agent_id=agent.id, claim_id=payload.claim_id,
        task=payload.task, status="running",
    )
    db.add(run)
    db.commit()
    try:
        client = OpenAI(api_key=settings.openai_api_key)
        prompt = payload.task
        if payload.source_urls:
            prompt += "\n\nSource URLs supplied by researcher (not assumed verified):\n" + "\n".join(str(url) for url in payload.source_urls)
        response = client.responses.create(
            model=settings.openai_model,
            instructions=build_system_prompt(agent),
            input=prompt,
            max_output_tokens=4000,
        )
        run.output = response.output_text
        run.status = "completed"
    except Exception as exc:
        run.status = "failed"
        # Do not return environment details or secrets to the client.
        run.error = f"Research provider request failed ({type(exc).__name__})."
    run.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(run)
    if run.status == "failed":
        raise HTTPException(status_code=502, detail=run.error)
    return run
