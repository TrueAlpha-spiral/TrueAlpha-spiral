import pytest
import importlib.util
import importlib.machinery
import os
import sys
import unittest.mock

def load_higgs_bason():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "higgs bason DHSV1"))

    loader = importlib.machinery.SourceFileLoader("higgs_bason", script_path)
    spec = importlib.util.spec_from_loader("higgs_bason", loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules["higgs_bason"] = module

    sys.modules['matplotlib'] = unittest.mock.MagicMock()
    sys.modules['matplotlib.pyplot'] = unittest.mock.MagicMock()
    sys.modules['numpy'] = unittest.mock.MagicMock()

    loader.exec_module(module)

    return module

def test_run_command_prevents_injection():
    hb = load_higgs_bason()

    # We mock subprocess.Popen
    import subprocess
    original_popen = subprocess.Popen

    args_passed = []
    kwargs_passed = {}

    class MockPopen:
        def __init__(self, args, **kwargs):
            args_passed.append(args)
            kwargs_passed.update(kwargs)
            self.returncode = 0

        def wait(self):
            pass

    subprocess.Popen = MockPopen

    try:
        # Avoid print spam during tests
        hb.log_message = lambda *args, **kwargs: None

        hb.run_command("echo 'hello'; rm -rf /", wait=False)

        # In the fixed version, args should be a list, and shell should be False
        assert kwargs_passed.get("shell") == False, "shell=False must be set"
        assert isinstance(args_passed[0], list), "Command must be tokenized into a list"
        assert args_passed[0] == ["echo", "hello;", "rm", "-rf", "/"], "shlex.split should properly tokenize"
    finally:
        subprocess.Popen = original_popen
# Nonce: 96641
