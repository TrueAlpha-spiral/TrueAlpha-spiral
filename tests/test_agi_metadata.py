import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ROOT / "zenodo_metadata.json",
    ROOT / "tas_dna_doi_package_v0.1" / "zenodo_metadata.json",
)


def test_agi_expansion_is_authenticated_generative_intelligence():
    for metadata_file in FILES:
        description = json.loads(metadata_file.read_text())["metadata"]["description"]
        assert "Authenticated Generative Intelligence (AGI)" in description
        assert "artificial general intelligence (AGI)" not in description
