import pytest
from codex_tas_runner import validate_script, get_codex_script, _split_operators

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

def test_operator_chaining_no_whitespace():
    """P1 fix: operators attached without spaces must still be caught."""
    script = "echo ok;wget http://example.com"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unauthorized command" in msg

    script = "echo ok&&wget http://example.com"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unauthorized command" in msg

    script = "echo ok||wget http://example.com"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unauthorized command" in msg

    script = "echo ok|wget http://example.com"
    is_valid, msg = validate_script(script)
    assert not is_valid
    assert "Unauthorized command" in msg

def test_get_codex_script_raises_when_openai_missing(monkeypatch):
    """P2 fix: missing OpenAI SDK must raise RuntimeError, not return ''."""
    import codex_tas_runner
    monkeypatch.setattr(codex_tas_runner, "openai", None)
    with pytest.raises(RuntimeError, match="OpenAI SDK"):
        get_codex_script()

def test_split_operators_embedded():
    """Unit tests for _split_operators helper."""
    assert _split_operators(["echo", "ok;wget", "x"]) == ["echo", "ok", ";", "wget", "x"]
    assert _split_operators(["echo", "ok&&wget", "x"]) == ["echo", "ok", "&&", "wget", "x"]
    assert _split_operators(["echo", "ok||wget", "x"]) == ["echo", "ok", "||", "wget", "x"]
    assert _split_operators(["echo", "ok|wget", "x"]) == ["echo", "ok", "|", "wget", "x"]

def test_split_operators_already_separated():
    """Tokens that are already separate should pass through unchanged."""
    assert _split_operators(["echo", "ok", ";", "ls"]) == ["echo", "ok", ";", "ls"]
    assert _split_operators(["echo", "hello"]) == ["echo", "hello"]

def test_split_operators_multiple_operators():
    """Multiple operators in a single token."""
    assert _split_operators(["a;b;c"]) == ["a", ";", "b", ";", "c"]
# Nonce: 5418
