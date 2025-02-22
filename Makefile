install:
	python -m venv venv
	. venv/bin/activate; pip install -Ur requirements.txt

run:
	. venv/bin/activate; python main.py

server:
	. venv/bin/activate; python main.py --transport sse --port 8000

clean:
	rm -rf venv
	find -iname "*.pyc" -delete

.PHONY: clean install run server