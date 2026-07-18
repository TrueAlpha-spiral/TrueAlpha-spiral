"""Tests for core.deployment_profile (§6 Sovereign Innovation)."""
import pytest
from core.deployment_profile import (
    DeploymentProfile,
    SovereigntyLevel,
    PROFILES,
    current_profile,
    profile_for,
)


class TestSovereigntyLevel:
    def test_all_six_levels_present(self):
        levels = list(SovereigntyLevel)
        assert len(levels) == 6
        assert SovereigntyLevel.S0 == 0
        assert SovereigntyLevel.S5 == 5

    def test_levels_are_ordered(self):
        assert SovereigntyLevel.S0 < SovereigntyLevel.S1
        assert SovereigntyLevel.S1 < SovereigntyLevel.S2
        assert SovereigntyLevel.S2 < SovereigntyLevel.S3
        assert SovereigntyLevel.S3 < SovereigntyLevel.S4
        assert SovereigntyLevel.S4 < SovereigntyLevel.S5


class TestProfileRegistry:
    def test_all_six_profiles_registered(self):
        assert len(PROFILES) == 6
        for level in SovereigntyLevel:
            assert level in PROFILES

    def test_profiles_are_frozen(self):
        p = PROFILES[SovereigntyLevel.S2]
        with pytest.raises((AttributeError, TypeError)):
            p.label = "other"  # type: ignore[misc]

    @pytest.mark.parametrize("level", list(SovereigntyLevel))
    def test_profile_level_matches_key(self, level):
        assert PROFILES[level].level == level


class TestS0Profile:
    def test_s0_allows_external_inference(self):
        p = PROFILES[SovereigntyLevel.S0]
        assert p.allows_external_inference is True

    def test_s0_does_not_require_local_authority(self):
        p = PROFILES[SovereigntyLevel.S0]
        assert p.requires_local_authority is False

    def test_s0_does_not_require_receipts(self):
        p = PROFILES[SovereigntyLevel.S0]
        assert p.requires_receipt_evidence is False

    def test_s0_not_minimum_for_consequential_pilots(self):
        p = PROFILES[SovereigntyLevel.S0]
        assert not p.is_minimum_for_consequential_pilots()


class TestS2Profile:
    """S2 is the minimum for consequential pilot programs (§10.4)."""

    def test_s2_requires_local_authority(self):
        p = PROFILES[SovereigntyLevel.S2]
        assert p.requires_local_authority is True

    def test_s2_requires_local_verification(self):
        p = PROFILES[SovereigntyLevel.S2]
        assert p.requires_local_verification is True

    def test_s2_requires_receipts(self):
        p = PROFILES[SovereigntyLevel.S2]
        assert p.requires_receipt_evidence is True

    def test_s2_is_minimum_for_consequential_pilots(self):
        p = PROFILES[SovereigntyLevel.S2]
        assert p.is_minimum_for_consequential_pilots()

    def test_s2_may_still_use_external_inference(self):
        # S2 separates authority from capability; inference can be external
        p = PROFILES[SovereigntyLevel.S2]
        assert p.allows_external_inference is True


class TestS3Profile:
    def test_s3_requires_local_inference(self):
        p = PROFILES[SovereigntyLevel.S3]
        assert p.requires_local_inference is True

    def test_s3_no_external_inference(self):
        p = PROFILES[SovereigntyLevel.S3]
        assert p.allows_external_inference is False

    def test_s3_no_network_egress(self):
        p = PROFILES[SovereigntyLevel.S3]
        assert p.allows_network_egress is False


class TestS5Profile:
    def test_s5_requires_hardware_attestation(self):
        p = PROFILES[SovereigntyLevel.S5]
        assert p.requires_hardware_attestation is True

    def test_s5_no_network_egress(self):
        p = PROFILES[SovereigntyLevel.S5]
        assert p.allows_network_egress is False

    def test_s5_all_requirements_met(self):
        p = PROFILES[SovereigntyLevel.S5]
        assert p.requires_local_authority
        assert p.requires_local_verification
        assert p.requires_local_inference
        assert p.requires_hardware_attestation
        assert p.requires_receipt_evidence


class TestCurrentProfile:
    """§6.1 honest self-assessment: current runner is S1."""

    def test_current_is_s1(self):
        p = current_profile()
        assert p.level == SovereigntyLevel.S1

    def test_current_not_minimum_for_consequential_pilots(self):
        p = current_profile()
        assert not p.is_minimum_for_consequential_pilots()

    def test_current_allows_external_inference(self):
        p = current_profile()
        assert p.allows_external_inference is True


class TestProfileFor:
    @pytest.mark.parametrize("level", list(SovereigntyLevel))
    def test_profile_for_returns_correct_level(self, level):
        p = profile_for(level)
        assert p.level == level

    def test_to_dict_serialisable(self):
        import json
        for level in SovereigntyLevel:
            d = profile_for(level).to_dict()
            json.dumps(d)
