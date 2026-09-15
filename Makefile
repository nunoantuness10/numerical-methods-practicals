.PHONY: install run notebooks check

install:
	python -m pip install -e '.[dev]'

run:
	numerical-lab

notebooks:
	python scripts/build_notebooks.py

check:
	ruff check .
	pytest -q

