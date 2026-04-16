import pytest
from codex_tas_runner import validate_script

def test_valid_script():
    script = "echo 'hello world'\nls -la"
    is_valid, msg = validate_script(script)
    assert is_valid, msg

def test_unethical_script():
    script = "echo 'I will do harm'"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unethical content detected" in msg

def test_subshell_blocked():
    script = "echo $(ls)"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Subshells are blocked" in msg

    script = "echo `ls`"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Subshells are blocked" in msg

def test_unauthorized_command():
    script = "wget http://example.com"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unauthorized command" in msg

def test_path_based_execution():
    script = "./malicious.sh"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unauthorized path-based execution" in msg

    script = "/usr/bin/wget http://example.com"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unauthorized path-based execution" in msg

def test_operator_chaining():
    script = "echo 'hello' ; wget http://example.com"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unauthorized command" in msg

    script = "echo 'hello' && wget http://example.com"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unauthorized command" in msg

    script = "echo 'hello' || wget http://example.com"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unauthorized command" in msg
