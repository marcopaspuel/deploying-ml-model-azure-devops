.PHONY: install test run all shell

all: install test run

install:
	poetry install
test:
	poetry run python -m pytest
run:
	poetry run python src/main.py
shell:
	poetry shell
