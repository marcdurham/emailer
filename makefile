.PHONY: dev update init install travis run test tox lint cover upload clean

dev: install update tox lint cover

update:
	pipenv update
	ctags

init: install
	pipenv install --python 3.7 --dev

install:
	pip install --quiet --user --upgrade pipenv tox twine

travis:
	pip install --upgrade pipenv
	pipenv install --dev --skip-lock

run:
	pipenv run email -k testkey --date=2018-01-01 --test -v

test:
	pipenv run pytest tests

tox:
	tox

lint:
	pipenv run pylint emailer tests/*

cover:
	pipenv run coverage run -m pytest
	pipenv run coverage report

upload: install tox cover lint
	python3.7 setup.py sdist bdist_wheel
	twine upload dist/*
	make clean

clean:
	rm -rf build dist
