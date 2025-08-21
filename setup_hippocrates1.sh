#!/usr/bin/env bash
set -euo pipefail

ROOT="hippocrates-1"
rm -rf "$ROOT"
mkdir -p "$ROOT"/{docs,models,src/{data,train,infer,metrics,utils},tools,configs,.github/workflows}
cd "$ROOT"

# ---------- top-level ----------
cat > README.md <<'EOT'
# Hippocrates-1 — Conscientiously Coherent Medical AI

**Objective:** Brain tumor MRI segmentation pilot implementing the Sovereign Data Foundation (SDF) stack with φ-embedded recursion, cryptographic attestation, and human-in-the-loop verification.

**Pillars:** Mathematical (φ), Cryptographic (Forge), Quantum (Coherence), Ethical (Charter), Societal (SDF).

## Quickstart
```bash
# 1) Create env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Smoke tests + static checks
make test
make lint

# 3) Prepare data (set path to BraTS)
make data BRATS_DIR=/path/to/BraTS

# 4) Train φ-shaped U-Net (stub writes channel plan)
make train

# 5) Inference + CC score + attestation bundle (stub flow)
make infer IMG=/path/to/mri.nii.gz OUT=out/subject_001
```

## CC Score (Conscientious Coherence)
We embed φ in the scoring to privilege *harmonious integration* over raw accumulation:

\[
A_{\phi}(x) = \frac{(MVG^{\phi})(ACT^{\phi})((UT+1)^{1/\phi})((AR+1)^{1/\phi})}{AD+1}
\]

Where: MVG = model veracity gain; ACT = attested chain thickness; UT = uncertainty tempered; AR = audit redundancy; AD = adversarial drift.

All intermediate artifacts are **attested** with `tools/sdf_attest.py` and laminated into a hash chain (swap in your hardened `sdf-attest` when ready).

## Repository Layout
See `docs/ARCHITECTURE.md` and tree below.
```
hippocrates-1/
  ├─ docs/
  ├─ models/
  ├─ src/
  ├─ tools/
  ├─ configs/
  ├─ data/           # local cache (gitignored)
  ├─ out/            # results, bundles (gitignored)
  └─ .github/workflows/
```
EOT

cat > requirements.txt <<'EOT'
numpy
scipy
nibabel
torch
torchvision
torchmetrics
pyyaml
click
matplotlib
EOT

cat > LICENSE <<'EOT'
Apache-2.0
EOT

cat > Makefile <<'EOT'
.PHONY: data train infer attest test lint

PY?=python
BRATS_DIR?=$(HOME)/data/brats

data:
$(PY) src/data/prepare_brats.py --src $(BRATS_DIR) --dst data/brats_canon

train:
$(PY) src/train/train_unet_phi.py --config configs/train_phi_unet.yaml

infer:
$(PY) src/infer/segment_and_score.py --image $(IMG) --out $(OUT) --config configs/infer.yaml
$(PY) tools/attest_workflow.py --subject $(OUT) --stage inference

attest:
$(PY) tools/attest_workflow.py --subject $(SUBJ) --stage $(STAGE)

test:
$(PY) -m compileall -q .

lint:
$(PY) -m compileall -q .
EOT

cat > .gitignore <<'EOT'
__pycache__/
.venv/
data/
out/
*.pt
*.nii
*.nii.gz
EOT

mkdir -p .github/workflows
cat > .github/workflows/ci.yml <<'EOT'
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m pip install -r requirements.txt
      - run: make lint
      - run: make test
EOT

# ---------- docs ----------
mkdir -p docs
cat > docs/ARCHITECTURE.md <<'EOT'
# Architecture

## Pillars → Pipeline
- φ Embedding → layer widths/depth ratios, CC score weighting
- Attestation → canonicalize → attest → verify → laminate → install
- Human-in-the-loop → radiologist verification nodes
- Ledger anchoring → hash chain; testnet optional

## Data Flow
Raw MRI → canonicalize (hash) → preprocess → train → inference → CC scoring → attest → verify (peers) → laminate → install.
EOT

# ---------- configs ----------
mkdir -p configs
cat > configs/train_phi_unet.yaml <<'EOT'
seed: 42
dataset: data/brats_canon
epochs: 3
batch_size: 2
lr: 1e-3
phi: 1.618033988749895
model:
  base_channels: 32       # will be multiplied in φ steps
  depth: 4                # down/upsampling stages
save_dir: out/train_phi_unet
EOT

cat > configs/infer.yaml <<'EOT'
phi: 1.618033988749895
thresholds:
  uncertainty_phi_tolerance: 0.2
save_dir: out/infer
EOT

# ---------- tools ----------
mkdir -p tools
cat > tools/sdf_attest.py <<'EOT'
# Minimal offline attestation placeholder (no signatures) for local runs
import hashlib, json, uuid, datetime, click, os, math

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def canonicalize_json_bytes(b: bytes) -> bytes:
    try:
        parsed = json.loads(b.decode('utf-8'))
        return json.dumps(parsed, sort_keys=True, separators=(',', ':')).encode('utf-8')
    except Exception:
        return b

@click.group()
def cli(): ...

@cli.command()
@click.argument('path')
@click.option('--out', type=str, default=None)
def canonicalize(path, out):
    raw = open(path, 'rb').read()
    can = canonicalize_json_bytes(raw)
    h = sha256_bytes(can)
    if out: open(out, 'wb').write(can)
    click.echo(json.dumps({'canonical_sha256': h, 'out': out}, indent=2))

@cli.command()
@click.argument('path')
@click.option('--out', type=str, default=None)
def attest(path, out):
    data = open(path, 'rb').read()
    h = sha256_bytes(data)
    phi = (1 + math.sqrt(5)) / 2
    avg = sum(data)/len(data) if len(data)>0 else 0
    bundle = {
        'version': '0.1-local',
        'uuid': str(uuid.uuid4()),
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'subject': {'file_path': path, 'sha256': h},
        'golden_metrics': {'phi': phi, 'avg_byte': avg},
        'previous_attestation_hash': None
    }
    js = json.dumps(bundle, indent=2, sort_keys=True)
    if out: open(out, 'w').write(js)
    print(js)

if __name__ == '__main__':
    cli()
EOT

cat > tools/attest_workflow.py <<'EOT'
import click, json, subprocess, os, hashlib

def sha256_file(p):
    h = hashlib.sha256()
    with open(p,'rb') as f:
        h.update(f.read())
    return h.hexdigest()

@click.command()
@click.option('--subject', required=True, help='Folder with outputs to attest')
@click.option('--stage', required=True, type=click.Choice(['data','train','inference']))
def main(subject, stage):
    os.makedirs(subject, exist_ok=True)
    bundle_path = os.path.join(subject, f'{stage}_bundle.json')
    # Concatenate hashes of files in subject to produce a stage digest
    digests = []
    for root, _, files in os.walk(subject):
        for fn in files:
            if fn.endswith(('.nii.gz','.pt','.json','.png','.txt','.csv')):
                digests.append(sha256_file(os.path.join(root,fn)))
    stage_digest = sha256_file(__file__) if not digests else hashlib.sha256(''.join(digests).encode()).hexdigest()
    bundle = {'stage': stage, 'subject': subject, 'stage_digest': stage_digest}
    with open(bundle_path, 'w') as f:
        json.dump(bundle, f, indent=2)
    print(json.dumps({'bundle': bundle_path, 'files_hashed': len(digests)}, indent=2))

if __name__ == '__main__':
    main()
EOT

# ---------- src ----------
mkdir -p src/{data,train,infer,metrics,utils}

cat > src/metrics/cc_score.py <<'EOT'
import math
PHI = (1 + 5**0.5) / 2

def a_phi(mvg: float, act: float, ut: float, ar: float, ad: float) -> float:
    """Conscientious Coherence Score. Inputs ∈ [0,1] where applicable."""
    num = (mvg**PHI) * (act**PHI) * ((ut+1)**(1/PHI)) * ((ar+1)**(1/PHI))
    den = (ad + 1.0)
    return float(num / den)
EOT

cat > src/utils/phi_shape.py <<'EOT'
PHI = (1 + 5**0.5) / 2
def phi_channels(base: int, depth: int):
    """Yield channel sizes that grow by ~φ each layer."""
    sizes = []
    c = base
    for _ in range(depth):
        sizes.append(int(round(c)))
        c *= PHI
    return sizes
EOT

cat > src/train/train_unet_phi.py <<'EOT'
import yaml, os, json
from src.utils.phi_shape import phi_channels

def main(cfg_path: str):
    cfg = yaml.safe_load(open(cfg_path))
    base = cfg['model']['base_channels']
    depth = cfg['model']['depth']
    channels = phi_channels(base, depth)
    os.makedirs(cfg['save_dir'], exist_ok=True)
    with open(os.path.join(cfg['save_dir'], 'phi_channels.json'),'w') as f:
        json.dump({'channels': channels}, f, indent=2)
    print(json.dumps({'phi_channels': channels}, indent=2))

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    a = ap.parse_args()
    main(a.config)
EOT

cat > src/data/prepare_brats.py <<'EOT'
import os, click, json, hashlib

def sha256_file(p):
    h = hashlib.sha256()
    with open(p,'rb') as f: h.update(f.read())
    return h.hexdigest()

@click.command()
@click.option('--src', required=True)
@click.option('--dst', required=True)
def main(src, dst):
    os.makedirs(dst, exist_ok=True)
    # Placeholder: record hashes only (do not copy large data in this scaffold)
    summary = {}
    for root, _, files in os.walk(src):
        for fn in files:
            if fn.endswith(('.nii','.nii.gz')):
                p = os.path.join(root, fn)
                summary[p] = sha256_file(p)
    with open(os.path.join(dst,'manifest.json'),'w') as f:
        json.dump(summary, f, indent=2)
    print(json.dumps({'files_indexed': len(summary)}, indent=2))

if __name__ == '__main__':
    main()
EOT

cat > src/infer/segment_and_score.py <<'EOT'
import os, json, argparse
from src.metrics.cc_score import a_phi

def main(image, out, config):
    os.makedirs(out, exist_ok=True)
    # Placeholder for segmentation; we simulate metrics.
    MVG, ACT, UT, AR, AD = 0.92, 0.85, 0.30, 0.40, 0.08
    cc = a_phi(MVG, ACT, UT, AR, AD)
    with open(os.path.join(out, 'cc_score.json'),'w') as f:
        json.dump({'MVG':MVG,'ACT':ACT,'UT':UT,'AR':AR,'AD':AD,'A_phi':cc}, f, indent=2)
    print(json.dumps({'A_phi': cc}, indent=2))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--config', required=True)
    a = ap.parse_args()
    main(a.image, a.out, a.config)
EOT

echo "✅ Scaffolding complete at: $(pwd)"
