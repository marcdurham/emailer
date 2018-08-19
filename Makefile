.PHONY: dev test lint upload clean
dev:
	pip install -U -r requirements.txt
	pip install -U -e .
	ctags

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
