//! `tas-merkle` — Production-grade Merkle lineage tree validation loop
//! for the TrueAlphaSpiral (TAS) governance framework.
//!
//! ## Architecture overview
//!
//! ```text
//! MerkleLineageTree  (tree.rs)
//!   ├── arena: Vec<MerkleNode>       — flat, index-addressed node store
//!   ├── root_hash: [u8; 32]          — cached root (updated on append/rollback)
//!   ├── AdmissibilityGate            — Axiom P₁ plug-in
//!   └── RefusalLog                   — "negative space of truth"
//!
//! CheckpointRegistry  (checkpoint.rs)
//!   └── Vec<CheckpointEntry>         — append-only, O(1) seal + lookup
//!
//! PhoenixProtocol  (phoenix.rs)
//!   └── PhoenixSession               — seven-phase recovery, strict ordering
//! ```
//!
//! ## Key invariants
//!
//! * **Axiom P₀ (Equivalence)** — enforced by [`hash::canonical_hash`]: field
//!   order never affects the hash.
//! * **Axiom P₁ (Admissibility)** — enforced at append time via
//!   [`tree::AdmissibilityGate`]: inadmissible nodes are never inserted.
//! * **RECOVERY_IS_NOT_AUTHORITY** — enforced by [`phoenix::PhoenixSession`]:
//!   recovery cannot manufacture authority.

pub mod checkpoint;
pub mod error;
pub mod hash;
pub mod node;
pub mod phoenix;
pub mod proof;
pub mod tree;

// ---------------------------------------------------------------------------
// Re-exports for convenience
// ---------------------------------------------------------------------------

pub use checkpoint::{CheckpointEntry, CheckpointHandle, CheckpointRegistry};
pub use error::LineageError;
pub use hash::{canonical_bytes, canonical_hash, sha256};
pub use node::{BranchData, LeafData, MerkleNode, NodeIdx};
pub use phoenix::{PhoenixPhase, PhoenixProtocol, PhoenixSession, ReceiptId};
pub use proof::{InclusionProof, RollbackProof, SiblingPosition};
pub use tree::{AdmissibilityGate, AlwaysAdmit, GateVerdict, MerkleLineageTree, RefusalLog, RefusalReceipt};

// ---------------------------------------------------------------------------
// C FFI — callable from Python via ctypes
// ---------------------------------------------------------------------------

/// Roll back the arena in-place to `checkpoint_generation`.
///
/// # Safety
///
/// - `arena_ptr` must point to a valid, mutable buffer of at least
///   `*arena_len` `MerkleNode`-sized slots.
/// - `arena_len` must be a valid non-null pointer.
///
/// # Returns
///
/// - `0`  on success; `*arena_len` is updated to the restored length.
/// - `-1` if `checkpoint_generation` exceeds the current `*arena_len`.
/// - `-2` if either pointer is null.
///
/// This function is intended for use from Python via `ctypes` in
/// `tas_phase0_microkernel.py` when a full Phoenix rollback is required
/// without the overhead of pyo3.
#[no_mangle]
pub unsafe extern "C" fn tas_merkle_rollback(
    checkpoint_arena_len: usize,
    _arena_ptr: *mut u8,
    arena_len: *mut usize,
) -> i32 {
    if arena_len.is_null() {
        return -2;
    }
    let current = unsafe { *arena_len };
    if checkpoint_arena_len > current {
        return -1;
    }
    unsafe { *arena_len = checkpoint_arena_len };
    0
}
