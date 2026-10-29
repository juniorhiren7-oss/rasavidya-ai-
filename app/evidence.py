from typing import Mapping

DIMENSIONS = (
    "source_authenticity",
    "translation_reliability",
    "historical_context",
    "chemical_plausibility",
    "analytical_quality",
    "independent_replication",
    "contamination_exclusion",
    "nuclear_origin_evidence",
)
VALID_STATES = {"not_assessed", "weak", "partial", "supported", "strong", "contradicted"}


def validate_evidence_states(values: Mapping[str, str]) -> dict[str, str]:
    normalized = {key: values.get(key, "not_assessed") for key in DIMENSIONS}
    unknown = {key: value for key, value in normalized.items() if value not in VALID_STATES}
    if unknown:
        raise ValueError(f"Invalid evidence state(s): {sorted(unknown)}")
    return normalized


def meets_transmutation_evidence_gate(values: Mapping[str, str]) -> bool:
    """A minimum review gate, not an automatic declaration that transmutation occurred."""
    evidence = validate_evidence_states(values)
    required = (
        "source_authenticity",
        "translation_reliability",
        "analytical_quality",
        "independent_replication",
        "contamination_exclusion",
        "nuclear_origin_evidence",
    )
    return all(evidence[key] == "strong" for key in required) and evidence["chemical_plausibility"] != "contradicted"
