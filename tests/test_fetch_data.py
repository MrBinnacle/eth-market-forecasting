import sys
import types
from unittest.mock import Mock, patch

# Provide minimal stubs for optional dependencies
if 'requests' not in sys.modules:
    requests_stub = types.ModuleType('requests')
    class RequestException(Exception):
        pass
    requests_stub.exceptions = types.SimpleNamespace(RequestException=RequestException)
    requests_stub.get = lambda *a, **k: None
    sys.modules['requests'] = requests_stub

if 'pandas' not in sys.modules:
    sys.modules['pandas'] = types.ModuleType('pandas')

if 'dotenv' not in sys.modules:
    dotenv_stub = types.ModuleType('dotenv')
    dotenv_stub.load_dotenv = lambda *a, **k: None
    sys.modules['dotenv'] = dotenv_stub

from backend.data_pipeline.fetch_data import fetch_market_share, fetch_gas_price


def test_fetch_market_share_success():
    expected = {"result": {"rows": [{"market": "dex"}]}}
    mock_resp = Mock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = expected
    with patch('backend.data_pipeline.fetch_data.requests.get', return_value=mock_resp) as mock_get:
        result = fetch_market_share('dex', 'ethereum')
    assert result == expected
    mock_get.assert_called_once()


def test_fetch_gas_price_success():
    api_data = {
        "status": "1",
        "result": {
            "SafeGasPrice": "10",
            "ProposeGasPrice": "20",
            "FastGasPrice": "30"
        }
    }
    mock_resp = Mock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = api_data
    with patch('backend.data_pipeline.fetch_data.requests.get', return_value=mock_resp):
        result = fetch_gas_price()
    assert result == {"low": "10", "average": "20", "high": "30"}
