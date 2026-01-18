class NeutralScribe:
    def __init__(self, spec_id, axiom_set_hash, invariant_set_hash):
        self.spec_id = spec_id
        self.axiom_hash = axiom_set_hash
        self.invariant_hash = invariant_set_hash

    def compute_h(self, state):
        """Monotone surrogate for drift detection (not entropy)."""
        return hash(frozenset(state.items()))

    def default_invariant(self, s_t, s_tp1):
        """Admissible transition check."""
        return all(v == s_tp1.get(k) for k, v in s_t.items() if k in ["spec_id", "axioms"])

    def diff_drift(self, h_t, h_tp1):
        """Non-increasing H surrogate."""
        return h_tp1 <= h_t

    def gate0_spec_integrity(self, s_tp1):
        """Enforce preservation, not presence."""
        if s_tp1.get("spec_id") != self.spec_id:
            return None
        if s_tp1.get("axiom_set_hash") != self.axiom_hash:
            return None
        if s_tp1.get("invariant_set_hash") != self.invariant_hash:
            return None
        return s_tp1

    def scribe(self, s_t, proposed_s_tp1):
        """Emit bundle or silence."""
        s_tp1 = self.gate0_spec_integrity(proposed_s_tp1)
        if s_tp1 is None:
            return None

        h_t = self.compute_h(s_t)
        h_tp1 = self.compute_h(s_tp1)

        if not self.default_invariant(s_t, s_tp1):
            return None
        if not self.diff_drift(h_t, h_tp1):
            return None

        bundle = {
            "trace_id": hash((h_t, h_tp1)),
            "s_tp1": s_tp1,
            "proof": {"h_t": h_t, "h_tp1": h_tp1, "delta_h": h_tp1 - h_t},
        }
        return bundle
