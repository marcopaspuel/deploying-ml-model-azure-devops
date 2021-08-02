all: start-server run-client

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
