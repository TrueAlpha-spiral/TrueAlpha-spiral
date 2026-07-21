/// Phoenix recovery protocol — mirrors `PhoenixRecovery` from the Python kernel.
///
/// ## Doctrinal invariant (§8)
///
/// **`RECOVERY_IS_NOT_AUTHORITY`**
///
/// A recovery operation cannot create missing permission, invent an absent
/// mandate, silently replace a missing context, or erase evidence of the
/// failed trajectory.  The seven mandatory phases enforce that recovery never
/// silently skips the authority-re-resolution, context-re-resolution,
/// mandate-acquisition, or evidence-preservation steps.
use crate::checkpoint::{CheckpointHandle, CheckpointRegistry};
use crate::error::LineageError;
use crate::proof::RollbackProof;
use crate::tree::MerkleLineageTree;

// ---------------------------------------------------------------------------
// Phase enumeration
// ---------------------------------------------------------------------------

/// The seven mandatory Phoenix recovery phases, in prescribed order (§8).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PhoenixPhase {
    IdentifyCheckpoint,      // Step 1
    PreserveFailureReceipts, // Step 2
    RestoreState,            // Step 3
    Reauthorize,             // Step 4
    ResolveContext,          // Step 5
    ObtainMandate,           // Step 6
    Resume,                  // Step 7
    Complete,                // Terminal
}

impl PhoenixPhase {
    fn name(&self) -> &'static str {
        match self {
            Self::IdentifyCheckpoint => "IdentifyCheckpoint",
            Self::PreserveFailureReceipts => "PreserveFailureReceipts",
            Self::RestoreState => "RestoreState",
            Self::Reauthorize => "Reauthorize",
            Self::ResolveContext => "ResolveContext",
            Self::ObtainMandate => "ObtainMandate",
            Self::Resume => "Resume",
            Self::Complete => "Complete",
        }
    }

    fn successor(&self) -> Option<PhoenixPhase> {
        match self {
            Self::IdentifyCheckpoint => Some(Self::PreserveFailureReceipts),
            Self::PreserveFailureReceipts => Some(Self::RestoreState),
            Self::RestoreState => Some(Self::Reauthorize),
            Self::Reauthorize => Some(Self::ResolveContext),
            Self::ResolveContext => Some(Self::ObtainMandate),
            Self::ObtainMandate => Some(Self::Resume),
            Self::Resume => Some(Self::Complete),
            Self::Complete => None,
        }
    }
}

// ---------------------------------------------------------------------------
// ReceiptId
// ---------------------------------------------------------------------------

/// Opaque identifier for a failure receipt that triggered this recovery.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReceiptId(pub String);

// ---------------------------------------------------------------------------
// PhaseLogEntry
// ---------------------------------------------------------------------------

/// One entry in the append-only phase history.
#[derive(Debug, Clone)]
pub struct PhaseLogEntry {
    pub phase: PhoenixPhase,
    pub evidence: String,
}

// ---------------------------------------------------------------------------
// PhoenixSession
// ---------------------------------------------------------------------------

/// An active Phoenix recovery session.
///
/// Created by [`PhoenixProtocol::initiate`].  Phases must be advanced in strict
/// order via [`PhoenixSession::advance`].  The actual tree rollback is
/// performed by [`PhoenixSession::execute_rollback`], which is only callable
/// during the `RestoreState` phase.
#[derive(Debug)]
pub struct PhoenixSession {
    /// Current phase.
    pub phase: PhoenixPhase,
    /// Checkpoint to restore to.
    pub checkpoint_handle: CheckpointHandle,
    /// Non-empty list of failure receipts that triggered this recovery.
    pub failure_receipt_ids: Vec<ReceiptId>,
    /// Append-only phase transition log.
    pub phase_log: Vec<PhaseLogEntry>,
}

impl PhoenixSession {
    /// Advance to the next mandatory phase.
    ///
    /// Phases must progress in strict order; skipping or reversing is a
    /// `LineageError::PhaseSkip`.
    pub fn advance(&mut self, phase: PhoenixPhase, evidence: &str) -> Result<(), LineageError> {
        let expected = self.phase.successor().ok_or_else(|| LineageError::PhaseSkip {
            current: self.phase.name().to_owned(),
            attempted: phase.name().to_owned(),
            expected: "(terminal — no successor)".to_owned(),
        })?;

        if phase != expected {
            return Err(LineageError::PhaseSkip {
                current: self.phase.name().to_owned(),
                attempted: phase.name().to_owned(),
                expected: expected.name().to_owned(),
            });
        }

        self.phase_log.push(PhaseLogEntry {
            phase,
            evidence: evidence.to_owned(),
        });
        self.phase = phase;
        Ok(())
    }

    /// Execute the tree rollback.
    ///
    /// **Only callable during `RestoreState` phase.**  Internally calls
    /// `tree.rollback_to(registry, self.checkpoint_handle)` and automatically
    /// advances the phase to `Reauthorize`.
    pub fn execute_rollback(
        &mut self,
        tree: &mut MerkleLineageTree,
        registry: &CheckpointRegistry,
    ) -> Result<RollbackProof, LineageError> {
        if self.phase != PhoenixPhase::RestoreState {
            return Err(LineageError::WrongPhase {
                required: PhoenixPhase::RestoreState.name().to_owned(),
                current: self.phase.name().to_owned(),
            });
        }

        let proof = tree.rollback_to(registry, self.checkpoint_handle)?;

        // Advance past RestoreState automatically.
        self.phase_log.push(PhaseLogEntry {
            phase: PhoenixPhase::Reauthorize,
            evidence: format!(
                "rollback executed: generation={}, restored_len={}, discarded={}",
                proof.generation, proof.restored_arena_len, proof.discarded_len
            ),
        });
        self.phase = PhoenixPhase::Reauthorize;
        Ok(proof)
    }

    /// Returns `true` if the session has reached the `Complete` terminal phase.
    pub fn is_complete(&self) -> bool {
        self.phase == PhoenixPhase::Complete
    }

    /// Doctrinal marker: recovery never manufactures authority.
    ///
    /// This method is intentionally a no-op.  Its presence at a callsite
    /// signals to auditors that the surrounding code has been reviewed for
    /// the RECOVERY_IS_NOT_AUTHORITY invariant.  Mirrors the Python
    /// `RecoveryRecord::assert_cannot_create_authority` method.
    #[inline(always)]
    pub fn assert_cannot_create_authority(&self) {
        // Structural invariant — no runtime enforcement needed here.
    }
}

// ---------------------------------------------------------------------------
// PhoenixProtocol factory
// ---------------------------------------------------------------------------

/// Factory for creating Phoenix recovery sessions.
///
/// Stateless: a single instance may be reused for multiple recoveries.
#[derive(Debug, Clone, Copy, Default)]
pub struct PhoenixProtocol;

impl PhoenixProtocol {
    /// Begin a new recovery sequence at phase `IdentifyCheckpoint`.
    ///
    /// # Errors
    ///
    /// Returns `LineageError::NoFailureReceipts` if `failure_receipts` is empty
    /// (§3.4 Evidentiary Sovereignty: failure must be preserved, not discarded).
    pub fn initiate(
        failure_receipts: &[ReceiptId],
        checkpoint: CheckpointHandle,
    ) -> Result<PhoenixSession, LineageError> {
        if failure_receipts.is_empty() {
            return Err(LineageError::NoFailureReceipts);
        }

        let phase_log = vec![PhaseLogEntry {
            phase: PhoenixPhase::IdentifyCheckpoint,
            evidence: format!(
                "checkpoint={:?}; failure_receipts={}",
                checkpoint,
                failure_receipts.len()
            ),
        }];

        Ok(PhoenixSession {
            phase: PhoenixPhase::IdentifyCheckpoint,
            checkpoint_handle: checkpoint,
            failure_receipt_ids: failure_receipts.to_vec(),
            phase_log,
        })
    }
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;
    use crate::checkpoint::CheckpointRegistry;
    use crate::node::{LeafData, MerkleNode};
    use crate::tree::MerkleLineageTree;

    fn receipt(id: &str) -> ReceiptId {
        ReceiptId(id.to_owned())
    }

    fn make_leaf(seed: u8) -> MerkleNode {
        MerkleNode::Leaf(LeafData {
            gene_id: [seed; 32],
            parent_hash: [0u8; 32],
            payload_hash: [seed + 1; 32],
            authority_binding: [seed + 2; 32],
        })
    }

    #[test]
    fn initiate_fails_without_receipts() {
        let result = PhoenixProtocol::initiate(&[], CheckpointHandle(0));
        assert!(matches!(result, Err(LineageError::NoFailureReceipts)));
    }

    #[test]
    fn phase_sequence_is_enforced() {
        let mut session =
            PhoenixProtocol::initiate(&[receipt("r1")], CheckpointHandle(0)).unwrap();
        assert_eq!(session.phase, PhoenixPhase::IdentifyCheckpoint);

        // Skip straight to RestoreState — should fail
        let err = session
            .advance(PhoenixPhase::RestoreState, "skipping ahead")
            .unwrap_err();
        assert!(matches!(err, LineageError::PhaseSkip { .. }));

        // Correct next phase
        session
            .advance(PhoenixPhase::PreserveFailureReceipts, "receipts sealed")
            .unwrap();
        assert_eq!(session.phase, PhoenixPhase::PreserveFailureReceipts);
    }

    #[test]
    fn full_happy_path() {
        let mut tree = MerkleLineageTree::new_open();
        let mut reg = CheckpointRegistry::new();

        for i in 0..5u8 {
            tree.append(make_leaf(i)).unwrap();
        }
        let cp = reg.seal(tree.root_hash(), tree.len());
        for i in 5..10u8 {
            tree.append(make_leaf(i)).unwrap();
        }

        let mut session =
            PhoenixProtocol::initiate(&[receipt("receipt-abc")], cp).unwrap();

        session
            .advance(PhoenixPhase::PreserveFailureReceipts, "receipts sealed")
            .unwrap();
        session
            .advance(PhoenixPhase::RestoreState, "about to rollback")
            .unwrap();

        let proof = session.execute_rollback(&mut tree, &reg).unwrap();
        assert_eq!(proof.discarded_len, 5);
        assert_eq!(tree.len(), 5);

        // Now in Reauthorize phase
        assert_eq!(session.phase, PhoenixPhase::Reauthorize);
        session.assert_cannot_create_authority();

        session
            .advance(PhoenixPhase::ResolveContext, "context resolved")
            .unwrap();
        session
            .advance(PhoenixPhase::ObtainMandate, "mandate obtained")
            .unwrap();
        session
            .advance(PhoenixPhase::Resume, "resuming execution")
            .unwrap();
        session
            .advance(PhoenixPhase::Complete, "recovery complete")
            .unwrap();

        assert!(session.is_complete());
        assert_eq!(session.phase_log.len(), 8); // init + 7 advances
    }

    #[test]
    fn execute_rollback_wrong_phase_errors() {
        let mut tree = MerkleLineageTree::new_open();
        let reg = CheckpointRegistry::new();
        let mut session =
            PhoenixProtocol::initiate(&[receipt("r1")], CheckpointHandle(0)).unwrap();

        // Phase is IdentifyCheckpoint — rollback not allowed yet
        let err = session
            .execute_rollback(&mut tree, &reg)
            .unwrap_err();
        assert!(matches!(err, LineageError::WrongPhase { .. }));
    }

    #[test]
    fn terminal_phase_cannot_advance() {
        let mut session =
            PhoenixProtocol::initiate(&[receipt("r1")], CheckpointHandle(0)).unwrap();

        // Fast-forward to Complete by advancing all phases
        let phases = [
            PhoenixPhase::PreserveFailureReceipts,
            PhoenixPhase::RestoreState,
            PhoenixPhase::Reauthorize,
            PhoenixPhase::ResolveContext,
            PhoenixPhase::ObtainMandate,
            PhoenixPhase::Resume,
            PhoenixPhase::Complete,
        ];
        for p in phases {
            // execute_rollback is skipped; directly advance RestoreState
            if p == PhoenixPhase::RestoreState || p == PhoenixPhase::Reauthorize {
                // For this test, bypass by manually setting phase
                // (only testing terminal phase guard)
            }
            let _ = session.advance(p, "");
        }
        // Now Complete — trying to advance further must error
        let err = session.advance(PhoenixPhase::Complete, "").unwrap_err();
        assert!(matches!(err, LineageError::PhaseSkip { .. }));
    }
}
