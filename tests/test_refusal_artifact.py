"""Tests for tas_openai_bridge.refusal — §11 compliance.

§11: A system is self-similar when its *failures* preserve the same integrity
structure as its successes.  Every RefusalArtifact must carry all required
fields.
"""

import pytest
from tas_openai_bridge.refusal import RefusalArtifact


REQUIRED_SECTION_11_FIELDS = (
    "reason",           # reason for refusal
    "code",             # stable failure code
    "candidate_hash",   # candidate identity or hash
    "rule_version",     # governing rule version
    "parent_context",   # parent or evaluation context
    "decision_state",   # decision state
    "verifier",         # signer or verifier evidence
    "timestamp",        # durable chronology
    "refusal_receipt_id",  # self-addressed receipt
)


class TestSection11Compliance:
    def test_basic_refusal_has_all_required_fields(self):
        artifact = RefusalArtifact(reason="test refusal")
        d = artifact.to_dict()
        for f in REQUIRED_SECTION_11_FIELDS:
            assert f in d, f"§11 field missing from refusal: {f}"

    def test_decision_state_is_always_refused(self):
        artifact = RefusalArtifact(reason="test")
        assert artifact.decision_state == "REFUSED"
        assert artifact.admissible is False

    def test_rule_version_is_set(self):
        artifact = RefusalArtifact(reason="test")
        assert artifact.rule_version  # non-empty

    def test_refusal_receipt_id_is_hash(self):
        artifact = RefusalArtifact(reason="test")._with_receipt_id()
        assert artifact.refusal_receipt_id.startswith("sha256:")

    def test_for_reason_convenience_constructor(self):
        artifact = RefusalArtifact.for_reason(
            "scope violation",
            code="TAS_SCOPE_ERROR",
            parent_context="gate:P0",
            verifier="TAS_ADMISSIBILITY_GATEWAY",
        )
        assert artifact.code == "TAS_SCOPE_ERROR"
        assert artifact.parent_context == "gate:P0"
        assert artifact.verifier == "TAS_ADMISSIBILITY_GATEWAY"
        assert artifact.refusal_receipt_id.startswith("sha256:")

    def test_to_dict_is_json_serialisable(self):
        import json
        artifact = RefusalArtifact.for_reason("test")
        # Must not raise
        json.dumps(artifact.to_dict())

    def test_candidate_hash_can_be_set(self):
        artifact = RefusalArtifact.for_reason("bad candidate",
                                               candidate_hash="sha256:" + "a" * 64)
        assert "sha256:" in artifact.candidate_hash


class TestBackwardCompatibility:
    """Existing callers that only set `reason` must not break."""

    def test_minimal_construction(self):
        artifact = RefusalArtifact(reason="oops")
        assert artifact.action == "REFUSE"
        assert artifact.admissible is False
        assert artifact.code == "TAS_OPENAI_REFUSAL"

    def test_to_dict_still_includes_action_and_admissible(self):
        d = RefusalArtifact(reason="oops").to_dict()
        assert d["action"] == "REFUSE"
        assert d["admissible"] is False
