import sys
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
    secured = secure_lineage(disclosure)
    assert "lineage" in secured
    assert secured["lineage"]["verified"]
