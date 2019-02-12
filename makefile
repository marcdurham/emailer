.PHONY: dev test_all init test lint cover upload clean travis

dev: test

init:
	pipenv install --python 3.7 --dev

test_all: test lint cover

test:
	pipenv run pytest tests

lint:
	pipenv run pylint emailer --rcfile emailer/.pylintrc
	#pipenv run pylint tests --rcfile tests/.pylintrc

cover:
	pipenv run coverage run -m pytest
	pipenv run coverage report

upload: test_all
	tox
	python3.7 setup.py sdist bdist_wheel
	twine upload dist/*
	make clean

clean:
	rm -rf build dist

travis:
	pip install --upgrade pipenv
	pipenv install --dev --skip-lock
