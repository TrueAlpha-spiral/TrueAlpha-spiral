import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import pytest
from hashlib import sha256

from tas_pythonetics.lineage_security import verify_tas_dna_lineage, secure_lineage
from tas_pythonetics import TAS_DNA


def test_verify_tas_dna_lineage():
    anchor = "test_anchor"
    assert verify_tas_dna_lineage(anchor, lambda a: sha256(TAS_DNA.encode()).hexdigest())
    assert not verify_tas_dna_lineage(anchor, lambda a: "tampered_hash")


def test_secure_lineage():
    disclosure = {"test": "data"}
    secured = secure_lineage(disclosure)
    assert "lineage" in secured
    assert secured["lineage"]["verified"]
