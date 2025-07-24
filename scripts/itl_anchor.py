import hashlib
import pathlib
import json
import datetime
try:
    import requests
except ImportError:  # Fallback to urllib if requests isn't installed
    requests = None
    import urllib.request

def sha_tree(root="tas_pythonetics"):
    h = hashlib.sha256()
    for p in sorted(pathlib.Path(root).rglob("*")):
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()

payload = {
    "hash": sha_tree(),
    "author": "Russell Nordland",
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    "version": "0.1.0",
}
# Replace with real TAS_ITL_API endpoint/token
def _post(url: str, data: dict):
    if requests:
        requests.post(url, json=data)
    else:
        encoded = json.dumps(data).encode()
        req = urllib.request.Request(
            url,
            data=encoded,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            resp.read()

_post("https://tas.itl/anchor", payload)
print("ITL anchor submitted:", payload["hash"])
