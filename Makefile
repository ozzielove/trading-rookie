.PHONY: setup test simulate

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	test -f .env || cp .env.example .env

test:
	PYTHONPATH=src .venv/bin/pytest -q

simulate:
	PYTHONPATH=src .venv/bin/python -m trading_rookie simulate
