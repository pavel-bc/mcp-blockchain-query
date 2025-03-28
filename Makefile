venv: venv/touchfile

venv/touchfile:
	test -d venv || virtualenv -p python3.13 venv
	. venv/bin/activate; pip install -e .
	touch venv/touchfile

run: venv
	. venv/bin/activate; python -m src.main

server: venv
	. venv/bin/activate; python -m src.main --transport sse --port 8000

inspect:
	npx @modelcontextprotocol/inspector node build/index.js

clean:
	rm -rf venv
	rm -rf src/__pycache__

.PHONY: inspect