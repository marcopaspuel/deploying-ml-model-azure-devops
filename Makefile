OWNER := marcopaspuel
PROJECT := deploying-ml-model-azure-devops
VERSION := 0.0.1
OPV := $(OWNER)/$(PROJECT):$(VERSION)

.PHONY: install
install:
	poetry install

.PHONY: start-server
start-server:
	poetry run python src/server.py

.PHONY: run-client
run-client:
	poetry run python src/client.py

.PHONY: test
test:
	poetry run python -m pytest

.PHONY: shell
shell:
	poetry shell

.PHONY: build
build:
	poetry export -o requirements.txt
	docker build -f docker/Dockerfile -t $(OPV) .
