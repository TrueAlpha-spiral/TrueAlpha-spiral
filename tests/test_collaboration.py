import pathlib
import pytest
import importlib.util
import importlib.abc
import sys

MODULE_PATH = pathlib.Path(__file__).resolve().parent / "collaboration"
if not MODULE_PATH.exists():
    MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "collaboration"

class StringLoader(importlib.abc.SourceLoader):
    def __init__(self, data, path):
        self.data = data
        self.path = path
    def get_source(self, fullname):
        return self.data
    def get_data(self, path):
        return self.data.encode('utf-8')
    def get_filename(self, fullname):
        return str(self.path)

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

    loader = StringLoader(code, path)
    spec = importlib.util.spec_from_loader("collaboration", loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules["collaboration"] = module
    loader.exec_module(module)
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
# Nonce: 9258
