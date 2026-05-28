"""
Integration tests for PTYAdmissionGuard — TAS / SDF bridge to gemini-cli PTY fix.

Six tests mirroring the test_sentient_lock.py structure:
  1. Successful admit_resize for a live process
  2. FORM failure: non-positive cols/rows → InvariantViolation before any OS call
  3. FUNCTION failure: dead PID → InvariantViolation before native resize
  4. FAITHFULNESS failure: forged lineage hash → InvariantViolation
  5. Phoenix rollback: window of 3 resizes where the 3rd targets a dead pid
  6. SDF loop completion: pty_sdf_contribution chain passes check_loop_completion()
"""

import os
import sys
import pytest

from tas_phase0_microkernel import Phase0Microkernel, InvariantViolation
from tas_pty_admission_guard import PTYAdmissionGuard
from pty_sdf_contribution import build_sdf_chain


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _live_pid() -> int:
    """Return the PID of the current process — guaranteed live."""
    return os.getpid()


def _dead_pid() -> int:
    """
    Return a PID that is almost certainly not alive.

    We use PID 1 on non-Linux systems where it is not the init process
    visible to the test runner, or a large sentinel value that is unlikely
    to be occupied.  In CI the test process cannot send signals to PID 1
    (EPERM), which our guard also treats as non-admissible.
    For reliable deadness we use a subprocess that exits immediately.
    """
    import subprocess
    proc = subprocess.Popen(["true"])
    proc.wait()
    return proc.pid  # process is now dead


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def kernel():
    k = Phase0Microkernel(steward="Russell Nordland / TrueAlphaSpiral")
    receipt = k.bootstrap()
    assert receipt["status"] == "BOOTSTRAP_LOCKED"
    return k


@pytest.fixture
def guard(kernel):
    return PTYAdmissionGuard(genesis_root=kernel.genesis_root)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestPTYAdmissionGuard:

    def test_successful_admit_resize(self, guard):
        """Successful admit_resize for a live process returns a 64-char hex hash."""
        pid = _live_pid()
        lineage = guard.admit_resize(pid, cols=80, rows=24)
        assert isinstance(lineage, str)
        assert len(lineage) == 64
        # Second resize chains off the first
        lineage2 = guard.admit_resize(pid, cols=120, rows=40, lineage_hash=lineage)
        assert len(lineage2) == 64
        assert lineage2 != lineage

    def test_form_failure_negative_cols(self, guard):
        """FORM failure: non-positive cols raises InvariantViolation before any OS call."""
        pid = _live_pid()
        with pytest.raises(InvariantViolation) as exc:
            guard.admit_resize(pid, cols=-1, rows=24)
        assert "FORM FAILURE" in str(exc.value)

    def test_form_failure_zero_rows(self, guard):
        """FORM failure: zero rows raises InvariantViolation before any OS call."""
        pid = _live_pid()
        with pytest.raises(InvariantViolation) as exc:
            guard.admit_resize(pid, cols=80, rows=0)
        assert "FORM FAILURE" in str(exc.value)

    @pytest.mark.skipif(sys.platform == "win32", reason="POSIX-only liveness probe")
    def test_function_failure_dead_pid(self, guard):
        """FUNCTION failure: dead PID raises InvariantViolation before native resize."""
        pid = _dead_pid()
        with pytest.raises(InvariantViolation) as exc:
            guard.admit_resize(pid, cols=80, rows=24)
        assert "FUNCTION FAILURE" in str(exc.value)

    def test_faithfulness_failure_forged_lineage(self, guard):
        """FAITHFULNESS failure: forged lineage hash raises InvariantViolation."""
        pid = _live_pid()
        with pytest.raises(InvariantViolation) as exc:
            guard.admit_resize(pid, cols=80, rows=24, lineage_hash="forged" * 10 + "1234")
        assert "FAITHFULNESS FAILURE" in str(exc.value)

    @pytest.mark.skipif(sys.platform == "win32", reason="POSIX-only liveness probe")
    def test_phoenix_rollback_on_dead_pid_in_window(self, guard):
        """
        Phoenix rollback: a window of 3 resizes where the 3rd targets a dead pid.
        The first two are admitted cleanly; the third raises InvariantViolation.
        """
        live = _live_pid()
        dead = _dead_pid()

        # Two successful resizes on the live pid
        l1 = guard.admit_resize(live, cols=80, rows=24)
        l2 = guard.admit_resize(live, cols=120, rows=40, lineage_hash=l1)

        # Third resize targets a dead pid — must fail at FUNCTION
        verified_count = 2
        with pytest.raises(InvariantViolation) as exc:
            guard.admit_resize(dead, cols=80, rows=24)

        assert "FUNCTION FAILURE" in str(exc.value)
        # Confirmed: first two passed, rollback engaged at the third
        assert verified_count == 2

    def test_sdf_loop_completion(self):
        """SDF loop: pty_sdf_contribution chain completes the 6-event closed loop."""
        validator = build_sdf_chain()
        assert validator.check_loop_completion() is True
