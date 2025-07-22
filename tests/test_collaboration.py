import pathlib
import types
import pytest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "collaboration"


def load_module(path: pathlib.Path):
    """Load the 'collaboration' script as a module despite non-Python preamble."""
    text = path.read_text()
    lines = text.splitlines()
    # Find the first line that looks like Python code
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("import") or line.startswith("from") or line.startswith("class"):
            start = i
            break
    code = "\n".join(lines[start:])
    module = types.ModuleType("collaboration")
    exec(code, module.__dict__)
    return module


collaboration = load_module(MODULE_PATH)
QuantumCollaborationInterface = collaboration.QuantumCollaborationInterface


@pytest.fixture
def qci():
    return QuantumCollaborationInterface()


def test_sequence_too_short(qci):
    result = qci._validate_helix_sequence("ATCG")
    assert result["valid"] is False
    assert result["reason"] == "Sequence too short"
    assert result["score"] == 0.2


def test_valid_sequence_no_quantum(qci):
    sequence = "ATCG01+-ATCG01+-"  # 8 valid complementary pairs
    result = qci._validate_helix_sequence(sequence)
    assert result["valid"] is True
    assert result["pair_validity"] == 1.0
    assert result["quantum_pattern_present"] is False
    assert result["score"] == 0.7


def test_valid_sequence_with_quantum(qci):
    sequence = "ATCG01+-ATCG01+-Q"  # valid pairs plus quantum marker
    result = qci._validate_helix_sequence(sequence)
    assert result["valid"] is True
    assert result["pair_validity"] == 1.0
    assert result["quantum_pattern_present"] is True
    assert result["score"] == 1.0


def test_invalid_sequence_insufficient_pairs(qci):
    sequence = "AACCGGTTAACCGGTTQ"  # No complementary pairs
    result = qci._validate_helix_sequence(sequence)
    assert result["valid"] is False
    assert result["score"] == pytest.approx(0.3)
    assert result["quantum_pattern_present"] is True
