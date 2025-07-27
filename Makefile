REGISTRY ?= your-docker-registry
IMAGE ?= coherence-api
TAG ?= $(shell git rev-parse --short HEAD)

build:
docker build -t $(REGISTRY)/$(IMAGE):$(TAG) .

push: build
docker push $(REGISTRY)/$(IMAGE):$(TAG)

helm-install:
helms upgrade --install coherence charts/coherence \
  --set image.repository=$(REGISTRY)/$(IMAGE) \
  --set image.tag=$(TAG)

helm-uninstall:
helms uninstall coherence

ci-gate:
covenant verify --phi-score 0.97 --phi-min 0.95 --ac-weight 0.9 --sc-weight 0.2
