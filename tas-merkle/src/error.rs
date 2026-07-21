/// All error types for the `tas-merkle` crate.
///
/// The verifier and tree operate **fail-closed**: every ambiguous or invalid
/// condition maps to a `LineageError` variant rather than a silent default.
use std::fmt;

/// Errors produced by the Merkle lineage tree and Phoenix recovery protocol.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LineageError {
    /// A node whose hash fields are internally inconsistent was presented.
    HashMismatch {
        expected: [u8; 32],
        got: [u8; 32],
    },

    /// The requested node index is outside the arena bounds.
    NodeNotFound { index: u64 },

    /// A leaf's parent hash does not match the hash of the node at the
    /// declared parent position.
    ParentLinkBroken {
        leaf_index: u64,
        expected_parent_hash: [u8; 32],
        got_parent_hash: [u8; 32],
    },

    /// The candidate node was rejected by the admissibility gate (Axiom P₁).
    Inadmissible { reason: String },

    /// The checkpoint handle does not correspond to any sealed checkpoint.
    UnknownCheckpoint { generation: u64 },

    /// Rollback was attempted but the checkpoint is ahead of the current tip.
    RollbackAheadOfTip {
        checkpoint_arena_len: usize,
        current_arena_len: usize,
    },

    /// A Phoenix phase was advanced out of order (skipped or reversed).
    PhaseSkip {
        current: String,
        attempted: String,
        expected: String,
    },

    /// Phoenix recovery was initiated without any failure receipts.
    /// §3.4 Evidentiary Sovereignty: failure must be preserved, not discarded.
    NoFailureReceipts,

    /// A Phoenix operation was attempted in a phase that does not permit it.
    WrongPhase { required: String, current: String },

    /// The rollback operation was attempted with an empty arena.
    EmptyArena,
}

impl fmt::Display for LineageError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::HashMismatch { expected, got } => write!(
                f,
                "hash mismatch: expected {}, got {}",
                hex(expected),
                hex(got)
            ),
            Self::NodeNotFound { index } => {
                write!(f, "node not found at arena index {index}")
            }
            Self::ParentLinkBroken {
                leaf_index,
                expected_parent_hash,
                got_parent_hash,
            } => write!(
                f,
                "parent link broken at leaf {leaf_index}: expected {}, got {}",
                hex(expected_parent_hash),
                hex(got_parent_hash)
            ),
            Self::Inadmissible { reason } => {
                write!(f, "node inadmissible (Axiom P₁): {reason}")
            }
            Self::UnknownCheckpoint { generation } => {
                write!(f, "no checkpoint for generation {generation}")
            }
            Self::RollbackAheadOfTip {
                checkpoint_arena_len,
                current_arena_len,
            } => write!(
                f,
                "checkpoint arena_len {checkpoint_arena_len} > current \
                 arena_len {current_arena_len}: cannot roll forward"
            ),
            Self::PhaseSkip {
                current,
                attempted,
                expected,
            } => write!(
                f,
                "phase skip: cannot advance from '{current}' to '{attempted}'; \
                 expected '{expected}'"
            ),
            Self::NoFailureReceipts => write!(
                f,
                "recovery requires at least one failure receipt \
                 (§3.4 Evidentiary Sovereignty)"
            ),
            Self::WrongPhase { required, current } => write!(
                f,
                "operation requires phase '{required}', but current phase is '{current}'"
            ),
            Self::EmptyArena => write!(f, "arena is empty; no nodes to operate on"),
        }
    }
}

impl std::error::Error for LineageError {}

fn hex(bytes: &[u8; 32]) -> String {
    bytes.iter().fold(String::with_capacity(64), |mut s, b| {
        use std::fmt::Write;
        let _ = write!(s, "{b:02x}");
        s
    })
}
