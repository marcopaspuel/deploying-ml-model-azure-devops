all: install start-server run-client test

install:
	poetry install
start-server:
	poetry run python src/server.py
run-client:
	poetry run python src/client.py
test:
	poetry run python -m pytest
shell:
	poetry shell

.PHONY: install start-server run-client test
