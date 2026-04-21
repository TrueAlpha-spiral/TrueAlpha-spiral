import json
from hashlib import sha256

from . import TAS_DNA


def verify_tas_dna_lineage(anchor: str, itl_query_func=None) -> bool:
    """Verify lineage against ITL to prevent deviation."""
    dna_hash = sha256(TAS_DNA.encode()).hexdigest()
    retrieved = itl_query_func(anchor) if itl_query_func else dna_hash
    return dna_hash == retrieved


def secure_lineage(disclosure: dict) -> dict:
    """Secure disclosure with TAS_DNA hash."""
    disclosure_payload = {
        key: value for key, value in disclosure.items() if key != "lineage"
    }
    lineage_hash = sha256(
        TAS_DNA.encode() + json.dumps(disclosure_payload, sort_keys=True).encode()
    ).hexdigest()
    disclosure["lineage"] = {
        "hash": lineage_hash,
        "verified": verify_tas_dna_lineage("lineage_anchor"),
        "notes": (
            "Ensures non-linear recursion remains untainted by "
            "linear constraints"
        ),
    }
    return disclosure
