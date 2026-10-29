"""Seed clearly caveated research leads; no verse transcription is asserted here."""
from app.database import SessionLocal, init_db
from app.models import EvidenceAssessment, HistoricalClaim, ResearchSource

SOURCES = [
    {
        "id": "src-rasarnavakalpa-1976",
        "title": "Rasārṇavakalpa (1976 edition catalogue record)",
        "authors": "Mira Roy; B. V. Subbarayappa",
        "publication_year": "1976",
        "source_type": "catalogue_record",
        "url": "https://wellcomecollection.org/works/zt6xu8ya",
        "notes": "Catalogue lead for the printed edition. The catalogue record is not a substitute for inspecting the printed Sanskrit passage.",
        "verification_status": "catalogue_located_text_not_yet_verified",
    },
    {
        "id": "src-deshpande-article",
        "title": "Vijaya Deshpande — historical analysis of Indian alchemy",
        "authors": "Vijaya Deshpande",
        "publication_year": "unknown",
        "source_type": "peer_reviewed_article",
        "url": "https://insa.nic.in/writereaddata/UpLoadedFiles/IJHS/Vol19_2_8_VDeshpande.pdf",
        "notes": "Scholarly secondary-source lead. Relevant claims still need precise page references and comparison with the primary edition.",
        "verification_status": "url_located_full_text_review_pending",
    },
    {
        "id": "src-ayuryog-reconstruction",
        "title": "AyurYog reconstruction discussion of Rasārṇava 12.51",
        "authors": "AyurYog",
        "publication_year": "unknown",
        "source_type": "experimental_reconstruction",
        "url": "https://ayuryog.org/blog/aurifiction-imitating-gold/",
        "notes": "Secondary reconstruction lead; does not independently establish elemental gold formation or nuclear transmutation.",
        "verification_status": "secondary_lead_not_independently_verified",
    },
]

CLAIMS = [
    {
        "id": "RKP-363",
        "title": "Rasārṇavakalpa verse 363 — reported copper-to-gold claim",
        "source_id": "src-rasarnavakalpa-1976",
        "reference": "verse 363",
        "classification": "claimed_elemental_transmutation",
        "summary": "Secondary transcriptions report a copper-to-gold claim. Exact Sanskrit wording, ingredients and context are not verified here; do not infer a procedure from this record.",
        "verification_status": "primary_text_verification_pending",
    },
    {
        "id": "RKP-404",
        "title": "Rasārṇavakalpa verse 404 — separate mercury-processing passage",
        "source_id": "src-rasarnavakalpa-1976",
        "reference": "verse 404",
        "classification": "mercury_processing_claim_unclassified",
        "summary": "Track as a separate passage. Intended outcome and wording must be established independently; do not combine it with verse 363.",
        "verification_status": "primary_text_verification_pending",
    },
    {
        "id": "R-12.51",
        "title": "Rasārṇava 12.51 — reconstruction lead",
        "source_id": "src-ayuryog-reconstruction",
        "reference": "12.51",
        "classification": "possible_alloy_or_surface_effect",
        "summary": "A secondary reconstruction discusses a gold-like result. Product composition and interpretation require independent verification; appearance alone is not elemental proof.",
        "verification_status": "secondary_reconstruction_review_pending",
    },
    {
        "id": "RPS-11.54",
        "title": "Rasaprakāśasudhākara 11.54 — secondary interpretation lead",
        "source_id": "src-deshpande-article",
        "reference": "11.54",
        "classification": "historical_claim_unclassified",
        "summary": "Seeded as a research lead only. Exact passage, translation, intended product and source page require confirmation before substantive conclusions.",
        "verification_status": "primary_text_verification_pending",
    },
]


def seed() -> None:
    init_db()
    with SessionLocal() as db:
        for record in SOURCES:
            if not db.get(ResearchSource, record["id"]):
                db.add(ResearchSource(**record))
        db.commit()
        for record in CLAIMS:
            if not db.get(HistoricalClaim, record["id"]):
                db.add(HistoricalClaim(**record))
        db.commit()
        assessments = [
            ("ea-rkp-363", "RKP-363", "not_assessed", "not_assessed", "partial", "partial"),
            ("ea-rkp-404", "RKP-404", "not_assessed", "not_assessed", "partial", "not_assessed"),
            ("ea-r-1251", "R-12.51", "partial", "partial", "supported", "supported"),
            ("ea-rps-1154", "RPS-11.54", "partial", "partial", "partial", "supported"),
        ]
        for item in assessments:
            assessment_id, claim_id, source, translation, context, chemistry = item
            if not db.get(EvidenceAssessment, assessment_id):
                db.add(EvidenceAssessment(
                    id=assessment_id, claim_id=claim_id,
                    source_authenticity=source, translation_reliability=translation,
                    historical_context=context, chemical_plausibility=chemistry,
                    rationale={"note": "Initial desk-level research lead only; not a verified experimental result."},
                    reviewer="seeded_scaffold",
                ))
        db.commit()
    print("Seeded 3 source leads, 4 separate historical claim records, and 4 caveated assessments.")


if __name__ == "__main__":
    seed()
