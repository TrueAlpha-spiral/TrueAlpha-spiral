import pytest
import os
import sys
import unittest.mock
import importlib.util
import importlib.machinery

@pytest.fixture(autouse=True)
def clean_sys_modules():
    with unittest.mock.patch.dict(sys.modules):
        yield

def load_itl_anchor():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "itl_anchor.py"))

    loader = importlib.machinery.SourceFileLoader("itl_anchor", script_path)
    spec = importlib.util.spec_from_loader("itl_anchor", loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules["itl_anchor"] = module

    requests_mock = unittest.mock.MagicMock()
    sys.modules["requests"] = requests_mock
    sys.modules["requests.exceptions"] = unittest.mock.MagicMock()

    return module, loader, requests_mock

def test_itl_anchor_success():
    module, loader, requests_mock = load_itl_anchor()

    mock_response = unittest.mock.MagicMock()
    requests_mock.post.return_value = mock_response

    with unittest.mock.patch.dict(os.environ, {"TAS_ITL_API_TOKEN": "test_token"}):
        loader.exec_module(module)

    requests_mock.post.assert_called_once()
    args, kwargs = requests_mock.post.call_args
    assert args[0] == "https://tas.itl/anchor"
    assert "json" in kwargs
    assert "timeout" in kwargs
    assert kwargs["timeout"] == 10
    assert "hash" in kwargs["json"]
    assert "author" in kwargs["json"]
    assert "headers" in kwargs
    assert kwargs["headers"]["Authorization"] == "Bearer test_token"

    mock_response.raise_for_status.assert_called_once()

def test_itl_anchor_failure():
    module, loader, requests_mock = load_itl_anchor()

    mock_response = unittest.mock.MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")
    requests_mock.post.return_value = mock_response

    with pytest.raises(Exception, match="HTTP Error"):
        with unittest.mock.patch.dict(os.environ, {"TAS_ITL_API_TOKEN": "test_token"}):
            loader.exec_module(module)

# Nonce: 84042
