import pytest
from tas_logos_gatekeeper import LogosValidationLoop


def mock_system_harmony() -> bool:
    return True


@pytest.fixture
def logos_validator():
    # Calibrated floor for dense JSON payload properties
    return LogosValidationLoop(invariant_check=mock_system_harmony, min_density_floor=0.15)


class TestLogosValidationLoop:

    def test_canonical_logos_transition(self, logos_validator):
        """Asserts that highly optimized, dense payloads pass the cryptographic gate instantly."""
        current_hash = b"\x01" * 32
        pristine_manifest = {
            "lineage_parent_hash": b"\x01" * 32,
            "payload_vector": {"cmd": "ACTUATE", "target": "SDFRegistryAPI"},
        }

        authorized = logos_validator.evaluate_logos_bounds(
            current_hash, pristine_manifest, nonce=301
        )
        assert authorized is True

    def test_diluted_entropy_rejection(self, logos_validator):
        """Asserts that high-volume noise padding drops the density metric below the floor and freezes execution."""
        current_hash = b"\x01" * 32
        padded_manifest = {
            "lineage_parent_hash": b"\x01" * 32,
            "payload_vector": {
                "cmd": "ACTUATE",
                "noise_padding": "A" * 8000,  # Verbose repetition that dilutes structural density
            },
        }

        authorized = logos_validator.evaluate_logos_bounds(
            current_hash, padded_manifest, nonce=302
        )
        assert authorized is False
