venv/bin/activate:
	python -m venv venv

deps: venv/bin/activate
	./exec pip install -r requirements.txt
.PHONY: deps

freeze:
	./exec pip freeze > ./requirements.txt

up:
	./exec python application.py
.PHONY: up
