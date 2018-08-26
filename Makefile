dev: install
	ctags

install:
	pip install --user -U pipenv
	pipenv install --python 3.5 --dev --skip-lock

ci:
	pipenv run pytest tests

test:
	tox

lint:
	pipenv run pylint emailer tests

cover:
	pipenv run coverage run -m pytest
	pipenv run coverage report

upload: test lint cover
	pip install --user -U twine
	python setup.py sdist bdist_wheel
	twine upload dist/*
	make clean

clean:
	rm -rf build dist emailer.egg-info
