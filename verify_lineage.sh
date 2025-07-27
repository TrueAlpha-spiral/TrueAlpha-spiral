#!/usr/bin/env bash
set -e

echo "🔎 Verifying TAS Digital DNA timeline manifest…"

if sha256sum -c TAS_DNA_timeline.yaml.sha256; then
  echo "✅ Manifest integrity intact."
else
  echo "❌ Manifest hash mismatch! Timeline may have been tampered."
  exit 1
fi

echo "ℹ️  (Optionally) run OpenTimestamps or on-chain verification here."
