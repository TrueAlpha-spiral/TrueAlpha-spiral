/// Proof types produced by the lineage tree.
///
/// Both types are value objects (no heap-allocated fields beyond `Vec`s).
use crate::node::NodeIdx;
use serde::{Deserialize, Serialize};

/// Which side the sibling occupies in one step of the Merkle audit path.
///
/// In the append-only linear chain `root_n = branch(root_{n-1}, hash(node_n))`,
/// the accumulated root is always on the **left** and the newly appended node
/// hash is always on the **right**.  A leaf that is not the chain head will
/// therefore have its prefix-root sibling on the **left**, while all subsequent
/// node-hash siblings sit on the **right**.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SiblingPosition {
    /// The sibling is on the left; `current` hash goes on the right.
    Left,
    /// The sibling is on the right; `current` hash stays on the left.
    Right,
}

/// Proof that a leaf at `leaf_index` is included in the tree at `root_hash`.
///
/// Each element of `siblings` pairs a hash with its position relative to the
/// running hash during proof verification.  An empty `siblings` list means the
/// leaf is the sole element (its own root).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct InclusionProof {
    /// Index of the proved leaf in the arena.
    pub leaf_index: NodeIdx,
    /// Hash of the leaf node itself.
    pub leaf_hash: [u8; 32],
    /// Ordered `(sibling_hash, position)` pairs from leaf to root.
    pub siblings: Vec<([u8; 32], SiblingPosition)>,
    /// Computed root hash at proof time.
    pub root_hash: [u8; 32],
}

impl InclusionProof {
    /// Verify the proof by recomputing the root from the leaf and siblings.
    ///
    /// Returns `true` iff the recomputed root equals `self.root_hash`.
    pub fn verify(&self) -> bool {
        use crate::hash::canonical_hash;

        let mut current = self.leaf_hash;
        for (sibling, position) in &self.siblings {
            current = match position {
                SiblingPosition::Left => canonical_hash(&[
                    ("left_hash", sibling.as_ref()),
                    ("right_hash", current.as_ref()),
                ]),
                SiblingPosition::Right => canonical_hash(&[
                    ("left_hash", current.as_ref()),
                    ("right_hash", sibling.as_ref()),
                ]),
            };
        }
        current == self.root_hash
    }
}

/// Proof that the tree was rolled back to a specific checkpoint generation.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct RollbackProof {
    /// The checkpoint generation that was restored.
    pub generation: u64,
    /// Arena length after rollback (equals `CheckpointEntry.arena_len`).
    pub restored_arena_len: usize,
    /// Root hash after rollback (equals `CheckpointEntry.root_hash`).
    pub restored_root_hash: [u8; 32],
    /// Arena length that was discarded during rollback.
    pub discarded_len: usize,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::hash::canonical_hash;
    use crate::node::NodeIdx;

    #[test]
    fn inclusion_proof_verifies_single_leaf() {
        let leaf_hash = [1u8; 32];
        let proof = InclusionProof {
            leaf_index: NodeIdx(0),
            leaf_hash,
            siblings: vec![],
            root_hash: leaf_hash,
        };
        assert!(proof.verify());
    }

    #[test]
    fn inclusion_proof_verifies_with_right_sibling() {
        let leaf_hash = [1u8; 32];
        let sibling = [2u8; 32];
        let root_hash = canonical_hash(&[
            ("left_hash", leaf_hash.as_ref()),
            ("right_hash", sibling.as_ref()),
        ]);
        let proof = InclusionProof {
            leaf_index: NodeIdx(0),
            leaf_hash,
            siblings: vec![(sibling, SiblingPosition::Right)],
            root_hash,
        };
        assert!(proof.verify());
    }

    #[test]
    fn inclusion_proof_verifies_with_left_sibling() {
        let leaf_hash = [2u8; 32];
        let sibling = [1u8; 32];
        let root_hash = canonical_hash(&[
            ("left_hash", sibling.as_ref()),
            ("right_hash", leaf_hash.as_ref()),
        ]);
        let proof = InclusionProof {
            leaf_index: NodeIdx(1),
            leaf_hash,
            siblings: vec![(sibling, SiblingPosition::Left)],
            root_hash,
        };
        assert!(proof.verify());
    }

    #[test]
    fn tampered_proof_fails() {
        let leaf_hash = [1u8; 32];
        let sibling = [2u8; 32];
        let root_hash = canonical_hash(&[
            ("left_hash", leaf_hash.as_ref()),
            ("right_hash", sibling.as_ref()),
        ]);
        let mut proof = InclusionProof {
            leaf_index: NodeIdx(0),
            leaf_hash,
            siblings: vec![(sibling, SiblingPosition::Right)],
            root_hash,
        };
        proof.leaf_hash[0] ^= 0xff; // tamper
        assert!(!proof.verify());
    }
}
