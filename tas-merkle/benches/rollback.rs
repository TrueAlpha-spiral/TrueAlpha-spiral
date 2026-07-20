/// Criterion benchmark: sub-millisecond rollback overhead.
///
/// Scenario: build a 10,000-node tree, seal a checkpoint, append 1,000 more
/// nodes, then measure the time to call `rollback_to`.
///
/// Target: p99 < 1 ms (typically < 300 ns on modern hardware for this
/// workload, because rollback is O(1): truncate + atomic root store).
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use tas_merkle::{
    CheckpointRegistry, LeafData, MerkleLineageTree, MerkleNode, NodeIdx,
};

fn make_leaf(seed: u8) -> MerkleNode {
    MerkleNode::Leaf(LeafData {
        gene_id: [seed; 32],
        parent_hash: [0u8; 32],
        payload_hash: [seed.wrapping_add(1); 32],
        authority_binding: [seed.wrapping_add(2); 32],
    })
}

fn bench_rollback(c: &mut Criterion) {
    let mut group = c.benchmark_group("rollback");
    group.sample_size(100);

    group.bench_function("rollback_10k_plus_1k", |b| {
        b.iter_with_setup(
            || {
                // Setup: build base tree + checkpoint + extra nodes.
                let mut tree = MerkleLineageTree::new_open();
                let mut reg = CheckpointRegistry::new();

                for i in 0..10_000u32 {
                    tree.append(make_leaf((i % 256) as u8)).unwrap();
                }
                let cp = reg.seal(tree.root_hash(), tree.len());

                for i in 0..1_000u32 {
                    tree.append(make_leaf((i % 256) as u8)).unwrap();
                }
                (tree, reg, cp)
            },
            |(mut tree, reg, cp)| {
                let proof = tree.rollback_to(&reg, black_box(cp)).unwrap();
                black_box(proof);
            },
        )
    });

    // Also bench the append path to establish a cost baseline.
    group.bench_function("append_single_leaf", |b| {
        let mut tree = MerkleLineageTree::new_open();
        let mut idx = 0u32;
        b.iter(|| {
            tree.append(black_box(make_leaf((idx % 256) as u8))).unwrap();
            idx += 1;
        });
    });

    // Bench verify_path on a 1,000-node tree.
    group.bench_function("verify_path_leaf0_of_1000", |b| {
        let mut tree = MerkleLineageTree::new_open();
        for i in 0..1_000u32 {
            tree.append(make_leaf((i % 256) as u8)).unwrap();
        }
        b.iter(|| {
            let proof = tree.verify_path(black_box(NodeIdx(0))).unwrap();
            black_box(proof);
        });
    });

    group.finish();
}

criterion_group!(benches, bench_rollback);
criterion_main!(benches);
