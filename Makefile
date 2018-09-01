dev: install
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
	pipenv run email

test:
	pipenv run pytest tests

tox:
	tox

lint:
	pipenv run pylint emailer tests

cover:
	pipenv run coverage run -m pytest
	pipenv run coverage report

upload: install test lint cover
	python3.7 setup.py sdist bdist_wheel
	twine upload dist/*
	make clean

clean:
	rm -rf build dist
