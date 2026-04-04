import os
import subprocess
import shlex
import pytest
import sys
import importlib.util

# Setup: prepare the target module for testing
def get_higgs_module():
    # We copied the file to a standard .py name for easier import
    import higgs_bason_dhsv1_temp as higgs
    return higgs

def teardown_module():
    if os.path.exists("VULNERABLE_TEST"):
        os.remove("VULNERABLE_TEST")
    if os.path.exists("higgs_bason_dhsv1_temp.py"):
        os.remove("higgs_bason_dhsv1_temp.py")

def test_command_injection_prevented():
    higgs = get_higgs_module()

    # Payload that would create a file if interpreted by shell
    payload = "echo 'vulnerable'; touch VULNERABLE_TEST"

    if os.path.exists("VULNERABLE_TEST"):
        os.remove("VULNERABLE_TEST")

    higgs.run_command(payload)

    assert not os.path.exists("VULNERABLE_TEST"), "Injection payload was executed by shell!"

def test_normal_command_works():
    higgs = get_higgs_module()

    # Simple echo command
    command = "echo 'hello world'"
    process = higgs.run_command(command)
    assert process.returncode == 0

def test_list_command_works():
    higgs = get_higgs_module()

    # Passing command as a list
    command = ["echo", "list command"]
    process = higgs.run_command(command)
    assert process.returncode == 0
