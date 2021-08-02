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

.PHONY: docker-build
docker-build:
	poetry export -o requirements.txt
	docker build -f docker/Dockerfile -t $(OPV) .

.PHONY: docker-run
docker-run:
	docker run --rm -d -p 8000:8000 -e DOCKER-SETUP=True --name api-server $(OPV)

.PHONY: docker-stop
docker-stop:
	docker stop api-server
