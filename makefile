.PHONY: dev test_all update init install travis run test lint cover upload clean

dev: install update test_all

test_all: test lint cover

update:
	pipenv update
	ctags

init: install
	pipenv install --python 3.7 --dev

install:
	pip install --quiet --user --upgrade pipenv tox twine wheel

travis:
	pip install --upgrade pipenv
	pipenv install --dev --skip-lock

run:
	pipenv run email --test -v -k testkey --date=$d

test:
	pipenv run pytest tests

lint:
	pipenv run pylint emailer tests/*

cover:
	pipenv run coverage run -m pytest
	pipenv run coverage report

upload: install test_all
	tox
	python3.7 setup.py sdist bdist_wheel
	twine upload dist/*
	make clean

clean:
	rm -rf build dist
