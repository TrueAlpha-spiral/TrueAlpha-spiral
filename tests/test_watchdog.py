import pathlib, sys
from fastapi.testclient import TestClient

# ensure repo root is on path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from main import app

client = TestClient(app)

def test_liveness():
    r = client.get('/watchdog/health/live')
    assert r.status_code == 200
    assert r.json()['status'] == 'alive'


def test_readiness():
    r = client.get('/watchdog/health/ready')
    assert r.status_code == 200
    assert r.json()['status'] == 'ready'
