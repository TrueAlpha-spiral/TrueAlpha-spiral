import pytest
from unittest.mock import patch, MagicMock
from codex_tas_runner import run_bash

@patch('subprocess.run')
@patch('shutil.which')
def test_run_bash_with_shutil_which(mock_which, mock_subprocess_run):
    mock_which.return_value = "/usr/bin/bash"
    mock_proc = MagicMock()
    mock_subprocess_run.return_value = mock_proc

    script = "echo test"
    result = run_bash(script)

    mock_which.assert_called_once_with("bash")
    mock_subprocess_run.assert_called_once_with(["/usr/bin/bash"], input=script, capture_output=True, text=True)
    assert result == mock_proc

@patch('subprocess.run')
@patch('shutil.which')
def test_run_bash_fallback(mock_which, mock_subprocess_run):
    mock_which.return_value = None
    mock_proc = MagicMock()
    mock_subprocess_run.return_value = mock_proc

    script = "echo fallback"
    result = run_bash(script)

    mock_which.assert_called_once_with("bash")
    mock_subprocess_run.assert_called_once_with(["/bin/bash"], input=script, capture_output=True, text=True)
    assert result == mock_proc
