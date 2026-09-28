import time
from sdf_tas_interface import SDFRegistryAPI, EpistemicCapsule

def test_sdf_registry_query_record_performance():
    registry = SDFRegistryAPI("witness-key")
    num_records = 1000
    created_ids = []
    for i in range(num_records):
        capsule = EpistemicCapsule(
            owner_id=f"user-{i}",
            claims=("claim",),
            sources=("source",),
            attestations=("attestation",),
            consent_scope="scope",
            revocation_policy="policy",
        )
        receipt = registry.notarize_capsule(capsule)
        rec_id = receipt["record_id"]
        created_ids.append(rec_id)
        registry.append_execution_record(rec_id, "exec-hash", "prev-hash", "EXECUTED")

    # Verify lookups
    sample_id = created_ids[500]
    records = registry.query_record(sample_id)
    assert len(records) == 2
    assert records[0]["record_id"] == sample_id
    assert records[1]["record_id"] == sample_id

    # Benchmark lookups
    num_queries = 2000
    start = time.perf_counter()
    for i in range(num_queries):
        target_id = created_ids[i % num_records]
        res = registry.query_record(target_id)
        assert len(res) == 2
    duration = time.perf_counter() - start

    assert duration < 0.05, f"Query took too long: {duration:.4f}s"
