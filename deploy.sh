#!/usr/bin/env bash
set -euo pipefail

REG=${REGISTRY:-your-docker-registry}
IMG=${IMAGE:-coherence-api}
TAG=$(git rev-parse --short HEAD)

docker build -t $REG/$IMG:$TAG .
docker push $REG/$IMG:$TAG

helm upgrade --install coherence charts/coherence \
  --set image.repository=$REG/$IMG \
  --set image.tag=$TAG
