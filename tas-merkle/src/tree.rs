/// `MerkleLineageTree` — append-only, arena-backed Merkle tree.
///
/// ## Design
///
/// Nodes are stored in a flat `Vec<MerkleNode>` (the arena).  The root is
/// tracked as a cached `[u8; 32]`.  Because the tree is append-only, rollback
/// is a pure `Vec::truncate` + root restoration — no rehashing.
///
/// Axiom P₁ (Admissibility) is enforced at append time via a pluggable
/// `AdmissibilityGate` trait.  Refused nodes are **not** inserted into the
/// arena; instead, a `RefusalReceipt` is appended to a separate, write-only
/// `RefusalLog` (the "negative space of truth").
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;

use crate::checkpoint::{CheckpointHandle, CheckpointRegistry};
use crate::error::LineageError;
use crate::node::{MerkleNode, NodeIdx};
use crate::proof::{InclusionProof, RollbackProof};

// ---------------------------------------------------------------------------
// Admissibility gate (Axiom P₁)
// ---------------------------------------------------------------------------

/// Result of an admissibility check.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GateVerdict {
    /// The node is admissible and may be inserted.
    Admit,
    /// The node is inadmissible for the given reason.
    Refuse(String),
}

/// Pluggable admissibility gate (Axiom P₁).
///
/// The default implementation (`AlwaysAdmit`) admits everything, suitable for
/// testing.  Production code should supply a gate that mirrors the nine-check
/// `UniversalVerifierKernel` logic.
pub trait AdmissibilityGate: Send + Sync {
    fn gate(&self, node: &MerkleNode) -> GateVerdict;
}

/// Trivial gate that admits every node — for tests and benchmarks only.
#[derive(Debug, Clone, Copy, Default)]
pub struct AlwaysAdmit;

impl AdmissibilityGate for AlwaysAdmit {
    fn gate(&self, _node: &MerkleNode) -> GateVerdict {
        GateVerdict::Admit
    }
}

// ---------------------------------------------------------------------------
// Refusal log
// ---------------------------------------------------------------------------

/// An immutable receipt produced when a node is refused by the gate.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RefusalReceipt {
    /// Hash of the refused node.
    pub refused_hash: [u8; 32],
    /// Human-readable reason from the gate.
    pub reason: String,
}

/// Append-only log of refusal receipts ("negative space of truth").
#[derive(Debug, Default)]
pub struct RefusalLog {
    receipts: Vec<RefusalReceipt>,
}

impl RefusalLog {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn record(&mut self, refused_hash: [u8; 32], reason: String) {
        self.receipts.push(RefusalReceipt {
            refused_hash,
            reason,
        });
    }

    pub fn receipts(&self) -> &[RefusalReceipt] {
        &self.receipts
    }

    pub fn len(&self) -> usize {
        self.receipts.len()
    }

    pub fn is_empty(&self) -> bool {
        self.receipts.is_empty()
    }
}

// ---------------------------------------------------------------------------
// MerkleLineageTree
// ---------------------------------------------------------------------------

/// The root-hash version counter, shared via `Arc<AtomicU64>` so that
/// readers can obtain the latest root index without holding a write lock.
///
/// Stores the arena index of the most recently updated root node.
type AtomicRootIdx = Arc<AtomicU64>;

/// An append-only Merkle lineage tree backed by a flat arena.
///
/// Thread safety: `&mut MerkleLineageTree` operations (append, rollback) are
/// exclusive.  The atomic root index allows concurrent readers to observe the
/// current root hash without blocking writers.
pub struct MerkleLineageTree {
    /// Flat arena of all nodes.
    arena: Vec<MerkleNode>,
    /// Cached root hash — updated after every append or rollback.
    root_hash: [u8; 32],
    /// Atomic arena index of the current root node (u64::MAX = no root).
    root_idx_atomic: AtomicRootIdx,
    /// Admissibility gate (Axiom P₁).
    gate: Box<dyn AdmissibilityGate>,
    /// Write-only log of refusal receipts.
    pub refusal_log: RefusalLog,
}

impl std::fmt::Debug for MerkleLineageTree {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("MerkleLineageTree")
            .field("len", &self.arena.len())
            .field("root_hash", &hex(&self.root_hash))
            .finish()
    }
}

impl MerkleLineageTree {
    /// Create a new empty tree using the supplied admissibility gate.
    pub fn new(gate: impl AdmissibilityGate + 'static) -> Self {
        Self {
            arena: Vec::new(),
            root_hash: [0u8; 32],
            root_idx_atomic: Arc::new(AtomicU64::new(u64::MAX)),
            gate: Box::new(gate),
            refusal_log: RefusalLog::new(),
        }
    }

    /// Create a new tree that admits everything (tests / benchmarks only).
    pub fn new_open() -> Self {
        Self::new(AlwaysAdmit)
    }

    /// Current number of nodes in the arena.
    pub fn len(&self) -> usize {
        self.arena.len()
    }

    /// Returns `true` if the arena contains no nodes.
    pub fn is_empty(&self) -> bool {
        self.arena.is_empty()
    }

    /// Current root hash.  Returns `[0u8; 32]` when the tree is empty.
    pub fn root_hash(&self) -> [u8; 32] {
        self.root_hash
    }

    /// Append a node to the tree after passing the admissibility gate (P₁).
    ///
    /// On refusal, the arena is **not mutated** and a `RefusalReceipt` is
    /// recorded in `self.refusal_log`.  Returns
    /// `Err(LineageError::Inadmissible)` in that case.
    ///
    /// On admission, the node is pushed to the arena, the root hash is
    /// updated, and the arena index of the new node is returned.
    pub fn append(&mut self, node: MerkleNode) -> Result<NodeIdx, LineageError> {
        // --- Axiom P₁: admissibility check ---
        match self.gate.gate(&node) {
            GateVerdict::Admit => {}
            GateVerdict::Refuse(reason) => {
                self.refusal_log.record(node.compute_hash(), reason.clone());
                return Err(LineageError::Inadmissible { reason });
            }
        }

        let idx = self.arena.len() as u64;
        self.arena.push(node);

        // Recompute root: for the append-only path we simply track the
        // cumulative hash chain.  The root hash after appending node n is:
        //   if n == 0: hash(node)
        //   else:      branch_hash(prev_root, hash(node))
        let node_hash = node.compute_hash();
        self.root_hash = if idx == 0 {
            node_hash
        } else {
            use crate::hash::canonical_hash;
            canonical_hash(&[
                ("left_hash", self.root_hash.as_ref()),
                ("right_hash", node_hash.as_ref()),
            ])
        };
        self.root_idx_atomic.store(idx, Ordering::Release);
        Ok(NodeIdx(idx))
    }

    /// Retrieve a node by its arena index.
    pub fn get(&self, idx: NodeIdx) -> Option<&MerkleNode> {
        self.arena.get(idx.0 as usize)
    }

    /// Build an inclusion proof for the leaf at `leaf_idx`.
    ///
    /// The proof recomputes the hash chain from the leaf to the current root
    /// by replaying the cumulative hash strategy used in `append`.
    ///
    /// Returns `LineageError::NodeNotFound` if `leaf_idx` is out of bounds.
    pub fn verify_path(&self, leaf_idx: NodeIdx) -> Result<InclusionProof, LineageError> {
        let idx = leaf_idx.0 as usize;
        if idx >= self.arena.len() {
            return Err(LineageError::NodeNotFound { index: leaf_idx.0 });
        }

        let leaf_hash = self.arena[idx].compute_hash();

        // Replay the cumulative hash chain:
        //   root_0 = hash(node_0)
        //   root_n = branch(root_{n-1}, hash(node_n))      [prev root on LEFT]
        //
        // For leaf at `idx`:
        //  - If idx > 0: sibling = prefix_root_{idx-1}, position = Left
        //    (the leaf sits on the RIGHT side of that branch).
        //  - For each subsequent node i = idx+1 … n-1: sibling = hash(node_i),
        //    position = Right (running hash stays on the LEFT).

        // Recompute prefix root up to (but not including) leaf_idx.
        let prefix_root: Option<[u8; 32]> = if idx == 0 {
            None
        } else {
            let mut r = self.arena[0].compute_hash();
            for i in 1..idx {
                use crate::hash::canonical_hash;
                r = canonical_hash(&[
                    ("left_hash", r.as_ref()),
                    ("right_hash", self.arena[i].compute_hash().as_ref()),
                ]);
            }
            Some(r)
        };

        // Build sibling list with positions.
        let mut siblings: Vec<([u8; 32], crate::proof::SiblingPosition)> = Vec::new();
        let mut running = leaf_hash;

        if let Some(pr) = prefix_root {
            // prefix_root is on the LEFT; leaf_hash is on the RIGHT.
            siblings.push((pr, crate::proof::SiblingPosition::Left));
            use crate::hash::canonical_hash;
            running = canonical_hash(&[
                ("left_hash", pr.as_ref()),
                ("right_hash", running.as_ref()),
            ]);
        }
        // Combine with subsequent nodes — running is on the LEFT.
        for i in (idx + 1)..self.arena.len() {
            use crate::hash::canonical_hash;
            let next_hash = self.arena[i].compute_hash();
            siblings.push((next_hash, crate::proof::SiblingPosition::Right));
            running = canonical_hash(&[
                ("left_hash", running.as_ref()),
                ("right_hash", next_hash.as_ref()),
            ]);
        }

        // `running` should now equal self.root_hash.
        debug_assert_eq!(running, self.root_hash, "verify_path: chain broken");

        Ok(InclusionProof {
            leaf_index: leaf_idx,
            leaf_hash,
            siblings,
            root_hash: self.root_hash,
        })
    }

    /// Roll back the tree to the state captured in `checkpoint`.
    ///
    /// This is a pure truncation: `arena.truncate(checkpoint.arena_len)` and
    /// an atomic root-hash restore.  No rehashing is performed.
    ///
    /// Returns `LineageError::RollbackAheadOfTip` if the checkpoint records a
    /// larger arena than currently exists (cannot roll forward).
    pub fn rollback_to(
        &mut self,
        registry: &CheckpointRegistry,
        handle: CheckpointHandle,
    ) -> Result<RollbackProof, LineageError> {
        let entry = registry.get_or_err(handle)?;
        if entry.arena_len > self.arena.len() {
            return Err(LineageError::RollbackAheadOfTip {
                checkpoint_arena_len: entry.arena_len,
                current_arena_len: self.arena.len(),
            });
        }
        let discarded = self.arena.len() - entry.arena_len;
        self.arena.truncate(entry.arena_len);
        self.root_hash = entry.root_hash;
        let new_root_idx = if entry.arena_len == 0 {
            u64::MAX
        } else {
            (entry.arena_len - 1) as u64
        };
        self.root_idx_atomic.store(new_root_idx, Ordering::Release);
        Ok(RollbackProof {
            generation: entry.generation,
            restored_arena_len: entry.arena_len,
            restored_root_hash: entry.root_hash,
            discarded_len: discarded,
        })
    }
}

fn hex(b: &[u8; 32]) -> String {
    b.iter().fold(String::with_capacity(64), |mut s, byte| {
        use std::fmt::Write;
        let _ = write!(s, "{byte:02x}");
        s
    })
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;
    use crate::node::{BranchData, LeafData};

    fn make_leaf(seed: u8) -> MerkleNode {
        MerkleNode::Leaf(LeafData {
            gene_id: [seed; 32],
            parent_hash: [0u8; 32],
            payload_hash: [seed.wrapping_add(1); 32],
            authority_binding: [seed.wrapping_add(2); 32],
        })
    }

    #[test]
    fn append_single_node() {
        let mut tree = MerkleLineageTree::new_open();
        let idx = tree.append(make_leaf(1)).unwrap();
        assert_eq!(idx, NodeIdx(0));
        assert_eq!(tree.len(), 1);
        assert_ne!(tree.root_hash(), [0u8; 32]);
    }

    #[test]
    fn root_changes_on_append() {
        let mut tree = MerkleLineageTree::new_open();
        tree.append(make_leaf(1)).unwrap();
        let r1 = tree.root_hash();
        tree.append(make_leaf(2)).unwrap();
        let r2 = tree.root_hash();
        assert_ne!(r1, r2);
    }

    #[test]
    fn inadmissible_node_does_not_mutate_arena() {
        struct RejectAll;
        impl AdmissibilityGate for RejectAll {
            fn gate(&self, _: &MerkleNode) -> GateVerdict {
                GateVerdict::Refuse("test rejection".into())
            }
        }
        let mut tree = MerkleLineageTree::new(RejectAll);
        let result = tree.append(make_leaf(1));
        assert!(matches!(result, Err(LineageError::Inadmissible { .. })));
        assert_eq!(tree.len(), 0);
        assert_eq!(tree.refusal_log.len(), 1);
    }

    #[test]
    fn rollback_restores_state() {
        let mut tree = MerkleLineageTree::new_open();
        let mut reg = CheckpointRegistry::new();

        for i in 0..5u8 {
            tree.append(make_leaf(i)).unwrap();
        }
        let cp = reg.seal(tree.root_hash(), tree.len());
        let root_at_cp = tree.root_hash();
        let len_at_cp = tree.len();

        for i in 5..15u8 {
            tree.append(make_leaf(i)).unwrap();
        }
        assert_ne!(tree.root_hash(), root_at_cp);
        assert_eq!(tree.len(), 15);

        let proof = tree.rollback_to(&reg, cp).unwrap();
        assert_eq!(tree.len(), len_at_cp);
        assert_eq!(tree.root_hash(), root_at_cp);
        assert_eq!(proof.discarded_len, 10);
    }

    #[test]
    fn rollback_ahead_of_tip_is_error() {
        let mut tree = MerkleLineageTree::new_open();
        let mut reg = CheckpointRegistry::new();
        tree.append(make_leaf(1)).unwrap();
        tree.append(make_leaf(2)).unwrap();
        let cp = reg.seal(tree.root_hash(), tree.len()); // len=2
        // Now trim manually (simulate an earlier state)
        tree.arena.truncate(1);
        tree.root_hash = [0u8; 32];
        let result = tree.rollback_to(&reg, cp);
        assert!(matches!(result, Err(LineageError::RollbackAheadOfTip { .. })));
    }

    #[test]
    fn verify_path_single_node() {
        let mut tree = MerkleLineageTree::new_open();
        tree.append(make_leaf(7)).unwrap();
        let proof = tree.verify_path(NodeIdx(0)).unwrap();
        assert!(proof.verify());
        assert_eq!(proof.root_hash, tree.root_hash());
    }

    #[test]
    fn verify_path_first_of_many() {
        let mut tree = MerkleLineageTree::new_open();
        for i in 0..8u8 {
            tree.append(make_leaf(i)).unwrap();
        }
        let proof = tree.verify_path(NodeIdx(0)).unwrap();
        assert!(proof.verify(), "inclusion proof for leaf 0 must verify");
    }

    #[test]
    fn verify_path_last_of_many() {
        let mut tree = MerkleLineageTree::new_open();
        for i in 0..8u8 {
            tree.append(make_leaf(i)).unwrap();
        }
        let proof = tree.verify_path(NodeIdx(7)).unwrap();
        assert!(proof.verify(), "inclusion proof for last leaf must verify");
    }

    #[test]
    fn verify_path_out_of_bounds() {
        let tree = MerkleLineageTree::new_open();
        assert!(matches!(
            tree.verify_path(NodeIdx(0)),
            Err(LineageError::NodeNotFound { .. })
        ));
    }

    #[test]
    fn branch_node_can_be_appended() {
        let mut tree = MerkleLineageTree::new_open();
        tree.append(MerkleNode::Branch(BranchData {
            left_hash: [1u8; 32],
            right_hash: [2u8; 32],
        }))
        .unwrap();
        assert_eq!(tree.len(), 1);
    }
}
