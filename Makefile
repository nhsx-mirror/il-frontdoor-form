venv/bin/activate:
	python -m venv venv

deps: venv/bin/activate
	./exec pip install -r requirements.txt
.PHONY: deps

up:
	./exec python app.py
.PHONY: up