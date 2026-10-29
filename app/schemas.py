from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

EvidenceState = Literal["not_assessed", "weak", "partial", "supported", "strong", "contradicted"]
SourceType = Literal["primary_text", "peer_reviewed_article", "catalogue_record", "experimental_reconstruction", "archaeological_report", "other"]


class SourceCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    authors: str = Field(default="Unknown", max_length=240)
    publication_year: str = Field(default="Unknown", max_length=40)
    source_type: SourceType = "other"
    url: HttpUrl
    notes: str = Field(default="", max_length=3000)


class SourceRead(SourceCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
    verification_status: str
    created_at: datetime


class ClaimCreate(BaseModel):
    id: str = Field(min_length=2, max_length=80)
    title: str = Field(min_length=3, max_length=240)
    source_id: str | None = None
    reference: str = Field(default="", max_length=120)
    classification: str = Field(default="unclassified", max_length=80)
    summary: str = Field(default="", max_length=5000)


class ClaimRead(ClaimCreate):
    model_config = ConfigDict(from_attributes=True)
    verification_status: str
    created_at: datetime


class EvidenceAssessmentCreate(BaseModel):
    id: str = Field(min_length=2, max_length=80)
    claim_id: str = Field(min_length=2, max_length=80)
    source_authenticity: EvidenceState = "not_assessed"
    translation_reliability: EvidenceState = "not_assessed"
    historical_context: EvidenceState = "not_assessed"
    chemical_plausibility: EvidenceState = "not_assessed"
    analytical_quality: EvidenceState = "not_assessed"
    independent_replication: EvidenceState = "not_assessed"
    contamination_exclusion: EvidenceState = "not_assessed"
    nuclear_origin_evidence: EvidenceState = "not_assessed"
    rationale: dict = Field(default_factory=dict)
    reviewer: str = Field(default="unassigned", max_length=120)


class EvidenceAssessmentRead(EvidenceAssessmentCreate):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime


class ResearchRunRequest(BaseModel):
    agent_id: str
    task: str = Field(min_length=12, max_length=4000)
    claim_id: str | None = None
    source_urls: list[HttpUrl] = Field(default_factory=list, max_length=10)


class ResearchRunRead(BaseModel):
    id: str
    agent_id: str
    claim_id: str | None
    task: str
    status: str
    output: str | None = None
    error: str | None = None
    created_at: datetime
    completed_at: datetime | None = None
