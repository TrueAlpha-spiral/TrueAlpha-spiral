import sys
import json
from pathlib import Path
from hashlib import sha256

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))  # noqa: E402

from tas_pythonetics.lineage_security import (  # noqa: E402
    verify_tas_dna_lineage,
    secure_lineage,
)
from tas_pythonetics import TAS_DNA  # noqa: E402


def test_verify_tas_dna_lineage():
    anchor = "test_anchor"
    assert verify_tas_dna_lineage(
        anchor, lambda a: sha256(TAS_DNA.encode()).hexdigest()
    )
    assert not verify_tas_dna_lineage(anchor, lambda a: "tampered_hash")


def test_secure_lineage():
    disclosure = {"test": "data"}

    # Expected hash computation needs to happen before secure_lineage mutates disclosure
    expected_hash = sha256(
        TAS_DNA.encode() + json.dumps(disclosure).encode()
    ).hexdigest()

    # Store original reference to verify in-place modification
    original_id = id(disclosure)

    secured = secure_lineage(disclosure)

    # 1. Verify in-place modification and return
    assert id(secured) == original_id, "Dictionary should be modified in-place"

    # 2. Verify lineage structure exists
    assert "lineage" in secured

    # 3. Verify deterministic hash calculation
    assert secured["lineage"]["hash"] == expected_hash

    # 4. Verify verified is True
    assert secured["lineage"]["verified"] is True

    # 5. Verify the notes field is correctly populated
    expected_notes = (
        "Ensures non-linear recursion remains untainted by "
        "linear constraints"
    )
    assert secured["lineage"]["notes"] == expected_notes
