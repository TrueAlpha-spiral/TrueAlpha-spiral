/// `CheckpointRegistry` — O(1) sealing and lookup for rollback anchors.
///
/// A checkpoint captures the arena length and root hash at a specific
/// generation counter.  Because the arena is append-only (nodes are never
/// removed except via rollback), restoring a checkpoint is a pure truncation:
/// no rehashing required.
use crate::error::LineageError;
use serde::{Deserialize, Serialize};

/// Opaque handle referencing a sealed checkpoint by its generation number.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct CheckpointHandle(pub u64);

/// One sealed checkpoint entry.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct CheckpointEntry {
    /// Monotonically increasing generation counter (starts at 0).
    pub generation: u64,
    /// Root hash of the tree at seal time.
    pub root_hash: [u8; 32],
    /// Arena length at seal time.
    pub arena_len: usize,
}

/// Registry of sealed checkpoints.
///
/// Checkpoints are append-only: once sealed, a `CheckpointEntry` is never
/// modified or removed.  This preserves an unalterable audit trail.
#[derive(Debug, Default)]
pub struct CheckpointRegistry {
    entries: Vec<CheckpointEntry>,
    next_generation: u64,
}

impl CheckpointRegistry {
    /// Create an empty registry.
    pub fn new() -> Self {
        Self::default()
    }

    /// Seal the current tree state as a new checkpoint.
    ///
    /// # Parameters
    /// - `root_hash`: the tree's current root hash (caller obtains via
    ///   `MerkleLineageTree::root_hash`).
    /// - `arena_len`: the tree's current arena length (caller obtains via
    ///   `MerkleLineageTree::len`).
    ///
    /// Returns a `CheckpointHandle` that can later be passed to
    /// `MerkleLineageTree::rollback_to`.
    pub fn seal(&mut self, root_hash: [u8; 32], arena_len: usize) -> CheckpointHandle {
        let generation = self.next_generation;
        self.next_generation += 1;
        self.entries.push(CheckpointEntry {
            generation,
            root_hash,
            arena_len,
        });
        CheckpointHandle(generation)
    }

    /// Look up a sealed checkpoint by its handle.
    pub fn get(&self, handle: CheckpointHandle) -> Option<&CheckpointEntry> {
        // Entries are stored in insertion order with consecutive generations,
        // so the handle's generation is a direct index.
        self.entries.get(handle.0 as usize)
    }

    /// Return the number of sealed checkpoints.
    pub fn len(&self) -> usize {
        self.entries.len()
    }

    /// Return `true` if no checkpoints have been sealed.
    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    /// Return the most recently sealed checkpoint, if any.
    pub fn latest(&self) -> Option<&CheckpointEntry> {
        self.entries.last()
    }

    /// Retrieve a checkpoint entry, returning `LineageError::UnknownCheckpoint`
    /// if the handle is invalid.
    pub fn get_or_err(&self, handle: CheckpointHandle) -> Result<&CheckpointEntry, LineageError> {
        self.get(handle)
            .ok_or(LineageError::UnknownCheckpoint { generation: handle.0 })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn seal_and_retrieve() {
        let mut reg = CheckpointRegistry::new();
        let h0 = reg.seal([0u8; 32], 10);
        let h1 = reg.seal([1u8; 32], 20);

        let e0 = reg.get(h0).unwrap();
        assert_eq!(e0.generation, 0);
        assert_eq!(e0.arena_len, 10);
        assert_eq!(e0.root_hash, [0u8; 32]);

        let e1 = reg.get(h1).unwrap();
        assert_eq!(e1.generation, 1);
        assert_eq!(e1.arena_len, 20);
    }

    #[test]
    fn missing_handle_returns_none() {
        let reg = CheckpointRegistry::new();
        assert!(reg.get(CheckpointHandle(99)).is_none());
    }

    #[test]
    fn get_or_err_returns_error_for_missing() {
        let reg = CheckpointRegistry::new();
        assert!(matches!(
            reg.get_or_err(CheckpointHandle(0)),
            Err(LineageError::UnknownCheckpoint { generation: 0 })
        ));
    }

    #[test]
    fn latest_tracks_last_sealed() {
        let mut reg = CheckpointRegistry::new();
        assert!(reg.latest().is_none());
        reg.seal([5u8; 32], 5);
        reg.seal([7u8; 32], 7);
        assert_eq!(reg.latest().unwrap().root_hash, [7u8; 32]);
    }
}
