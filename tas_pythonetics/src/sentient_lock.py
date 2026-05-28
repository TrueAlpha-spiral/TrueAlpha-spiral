"""
Re-export shim so that ``from sentient_lock import SentientLock`` works when
``tas_pythonetics/src`` is on the Python path (as configured in pytest.ini).
"""
from tas_pythonetics.sentient_lock import SentientLock  # noqa: F401

__all__ = ["SentientLock"]
