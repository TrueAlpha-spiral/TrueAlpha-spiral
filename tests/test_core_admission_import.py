def test_authenticated_gate_is_importable_from_canonical_core_namespace():
    from admission_gate import AdmissionGatekeeper as CompatibilityGate
    from core.verification.admission_gate import AdmissionGatekeeper

    assert AdmissionGatekeeper is CompatibilityGate
