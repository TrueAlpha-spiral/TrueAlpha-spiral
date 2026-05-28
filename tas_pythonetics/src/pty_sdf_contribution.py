"""
Re-export shim so that ``from pty_sdf_contribution import build_sdf_chain``
works when ``tas-recursion-conversion`` is on the Python path (as configured
in pytest.ini).
"""
from tas_governance.core.invariants.pty_sdf_contribution import build_sdf_chain  # noqa: F401

__all__ = ["build_sdf_chain"]
