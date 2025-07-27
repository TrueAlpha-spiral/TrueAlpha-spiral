#!/usr/bin/env python3
"""Mint, seal, and verify TAS_DNA genes."""
import json
import hashlib
import datetime
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, Any, List
from jsonschema import validate

with open("tas_dna_gene.schema.json", "r") as f:
    GENE_SCHEMA = json.load(f)


@dataclass
class TASGene:
    gene_id: str
    uuid: str
    title: str
    author: str
    purpose: str
    timestamp_utc: str
    sealed: bool
    triad: Dict[str, Any]
    inputs: Dict[str, str]
    guards: List[str]
    core_equation: str
    outputs: Dict[str, str]
    immutables: Dict[str, Any]
    anchors: Dict[str, str]
    links: Dict[str, Any] | None = None
    defaults: Dict[str, Any] | None = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), separators=(",", ":"), sort_keys=True)


def mint_gene(base: Dict[str, Any]) -> TASGene:
    gene = TASGene(
        uuid=str(uuid.uuid4()),
        timestamp_utc=datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        sealed=False,
        **base,
    )
    validate(instance=asdict(gene), schema=GENE_SCHEMA)
    return gene


def sha256_gene(gene: TASGene) -> str:
    return hashlib.sha256(gene.to_json().encode()).hexdigest()


def mock_itl_anchor(gene_hash: str) -> str:
    return f"ITL::{gene_hash[:16]}"


def seal_gene(gene: TASGene) -> None:
    gene.sealed = True


def verify_runtime_action(*, auth_weight: float, subj_weight: float, phi_score: float, phi_min: float) -> None:
    if auth_weight <= subj_weight:
        raise ValueError("TAS violation: A_C must exceed S_C (A_C > S_C)")
    if phi_score < phi_min:
        raise ValueError(f"TAS violation: Φ {phi_score} below Φ_MIN {phi_min}")


if __name__ == "__main__":
    base = {
        "gene_id": "ALTR_LOG_KERNEL_v1",
        "title": "Log-scaled altruism kernel",
        "author": "Russell Nordland",
        "purpose": "Optimize collective utility via log compression.",
        "triad": {
            "T": {"equations": ["J = Σ w_i log(f_i + eps)"], "constants": {"eps": 1e-9}},
            "A": {"authors": ["Russell Nordland"], "signatures": ["TAS_HUMAN_SIG"]},
            "S": {"context": "Initial deployment", "state_vars": {"Φ_MIN": 0.95}},
        },
        "inputs": {"metrics": "dict[str->float]", "weights": "dict[str->float]"},
        "guards": ["A_C > S_C", "Φ_score >= Φ_MIN"],
        "core_equation": "J = Σ_i w_i * log(f_i + eps)",
        "outputs": {"J": "float", "action": "Any"},
        "immutables": {"hash_algo": "sha256", "version": 1},
        "anchors": {
            "parent_tas_dna_hash": "0x1234567890abcdef",
            "weights_source_hash": "0xfedcba9876543210",
        },
        "defaults": {"Φ_MIN": 0.95, "eps_floor": 1e-9},
    }

    gene = mint_gene(base)
    gene_hash = sha256_gene(gene)
    anchor_id = mock_itl_anchor(gene_hash)
    seal_gene(gene)

    print("GENE_HASH:", gene_hash)
    print("ANCHOR_ID:", anchor_id)

    verify_runtime_action(
        auth_weight=0.9,
        subj_weight=0.2,
        phi_score=0.97,
        phi_min=gene.defaults["Φ_MIN"],
    )
    print("Runtime verification passed ✓")
