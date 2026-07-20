/// `MerkleNode` — the fundamental storage unit of the lineage tree.
///
/// Two discriminants:
/// - `Leaf` — carries gene provenance fields; represents one `TASGene`.
/// - `Branch` — internal aggregation node; combines two child hashes.
///
/// All hash fields are `[u8; 32]` to avoid heap allocation per node.
/// `MerkleNode` is `Copy` so the arena can be cheaply cloned for
/// snapshot / rollback bookkeeping.
use crate::hash::canonical_hash;
use serde::{Deserialize, Serialize};

/// Opaque index into the `MerkleLineageTree` arena.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct NodeIdx(pub u64);

/// A single node stored in the arena.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum MerkleNode {
    /// A leaf node representing one `TASGene` transition unit.
    Leaf(LeafData),
    /// An internal branch node combining two child subtree hashes.
    Branch(BranchData),
}

/// All provenance fields for a `TASGene`-derived leaf.
///
/// Field sizes:
/// - `gene_id`:          32-byte SHA-256 of the gene's canonical content
/// - `parent_hash`:      32-byte hash of the parent leaf (`[0u8;32]` at genesis)
/// - `payload_hash`:     32-byte hash of the gene's `receipt` dict
/// - `authority_binding`: 32-byte hash of the `AuthoritySnapshot.snapshot_id`
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct LeafData {
    pub gene_id: [u8; 32],
    pub parent_hash: [u8; 32],
    pub payload_hash: [u8; 32],
    pub authority_binding: [u8; 32],
}

/// An internal branch combining two child subtree hashes.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct BranchData {
    pub left_hash: [u8; 32],
    pub right_hash: [u8; 32],
}

impl MerkleNode {
    /// Compute the canonical SHA-256 hash of this node (Axiom P₀).
    ///
    /// For a `Leaf`, hashes all four provenance fields by name.
    /// For a `Branch`, hashes the two child hashes by name.
    pub fn compute_hash(&self) -> [u8; 32] {
        match self {
            MerkleNode::Leaf(l) => canonical_hash(&[
                ("authority_binding", l.authority_binding.as_ref()),
                ("gene_id", l.gene_id.as_ref()),
                ("parent_hash", l.parent_hash.as_ref()),
                ("payload_hash", l.payload_hash.as_ref()),
            ]),
            MerkleNode::Branch(b) => canonical_hash(&[
                ("left_hash", b.left_hash.as_ref()),
                ("right_hash", b.right_hash.as_ref()),
            ]),
        }
    }

    /// Returns `true` if this node is a `Leaf`.
    pub fn is_leaf(&self) -> bool {
        matches!(self, MerkleNode::Leaf(_))
    }
}

// Safety: `[u8; 32]` is trivially `Send + Sync`; the enum is `Copy`.
unsafe impl Send for MerkleNode {}
unsafe impl Sync for MerkleNode {}

#[cfg(test)]
mod tests {
    use super::*;

    fn leaf(seed: u8) -> MerkleNode {
        MerkleNode::Leaf(LeafData {
            gene_id: [seed; 32],
            parent_hash: [0u8; 32],
            payload_hash: [seed.wrapping_add(1); 32],
            authority_binding: [seed.wrapping_add(2); 32],
        })
    }

    #[test]
    fn hash_is_deterministic() {
        let n = leaf(1);
        assert_eq!(n.compute_hash(), n.compute_hash());
    }

    #[test]
    fn distinct_leaves_have_distinct_hashes() {
        assert_ne!(leaf(1).compute_hash(), leaf(2).compute_hash());
    }

    #[test]
    fn branch_hash_deterministic() {
        let b = MerkleNode::Branch(BranchData {
            left_hash: [1u8; 32],
            right_hash: [2u8; 32],
        });
        assert_eq!(b.compute_hash(), b.compute_hash());
    }

    #[test]
    fn branch_left_right_order_matters() {
        let b1 = MerkleNode::Branch(BranchData {
            left_hash: [1u8; 32],
            right_hash: [2u8; 32],
        });
        let b2 = MerkleNode::Branch(BranchData {
            left_hash: [2u8; 32],
            right_hash: [1u8; 32],
        });
        // left_hash ≠ right_hash, so hashes differ even though field names
        // are sorted — the *values* differ.
        assert_ne!(b1.compute_hash(), b2.compute_hash());
    }
}
