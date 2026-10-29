from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ResearchSource(Base):
    __tablename__ = "research_sources"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    title: Mapped[str] = mapped_column(String(240), index=True)
    authors: Mapped[str] = mapped_column(String(240), default="Unknown")
    publication_year: Mapped[str] = mapped_column(String(40), default="Unknown")
    source_type: Mapped[str] = mapped_column(String(50), default="other")
    url: Mapped[str] = mapped_column(String(2000))
    notes: Mapped[str] = mapped_column(Text, default="")
    verification_status: Mapped[str] = mapped_column(String(50), default="unverified")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class HistoricalClaim(Base):
    __tablename__ = "historical_claims"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    title: Mapped[str] = mapped_column(String(240))
    source_id: Mapped[str | None] = mapped_column(ForeignKey("research_sources.id"), nullable=True)
    reference: Mapped[str] = mapped_column(String(120), default="")
    classification: Mapped[str] = mapped_column(String(80), default="unclassified")
    summary: Mapped[str] = mapped_column(Text, default="")
    verification_status: Mapped[str] = mapped_column(String(50), default="unverified")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class EvidenceAssessment(Base):
    __tablename__ = "evidence_assessments"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    claim_id: Mapped[str] = mapped_column(ForeignKey("historical_claims.id"), index=True)
    source_authenticity: Mapped[str] = mapped_column(String(24), default="not_assessed")
    translation_reliability: Mapped[str] = mapped_column(String(24), default="not_assessed")
    historical_context: Mapped[str] = mapped_column(String(24), default="not_assessed")
    chemical_plausibility: Mapped[str] = mapped_column(String(24), default="not_assessed")
    analytical_quality: Mapped[str] = mapped_column(String(24), default="not_assessed")
    independent_replication: Mapped[str] = mapped_column(String(24), default="not_assessed")
    contamination_exclusion: Mapped[str] = mapped_column(String(24), default="not_assessed")
    nuclear_origin_evidence: Mapped[str] = mapped_column(String(24), default="not_assessed")
    rationale: Mapped[dict] = mapped_column(JSON, default=dict)
    reviewer: Mapped[str] = mapped_column(String(120), default="unassigned")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class ResearchRun(Base):
    __tablename__ = "research_runs"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    agent_id: Mapped[str] = mapped_column(String(80), index=True)
    claim_id: Mapped[str | None] = mapped_column(ForeignKey("historical_claims.id"), nullable=True)
    task: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    output: Mapped[str | None] = mapped_column(Text, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
