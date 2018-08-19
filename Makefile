.PHONY: dev install test lint upload clean
dev:
	ctags

install:
	pip install -U -r requirements.txt
	pip install -U -e .

test:
	pytest

lint:
	pylint emailer tests

upload: test lint
	./setup.py sdist bdist_wheel
	twine upload dist/*
	make clean

clean:
	rm -rf build
	rm -rf dist
