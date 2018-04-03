dev:
	pip install -e .

full: test integration_test lint

test: unit_test

lint: pylint

integration_test:
	tests/integration_test.py

unit_test:
	tests/unit_test.py

pylint:
	pylint emailer tests/*.py

upload: full setup pypi clean

setup:
	pandoc README.md --from markdown --to rst -s -o README.rst
	./setup.py sdist bdist_wheel

pypi:
	twine upload dist/*

clean:
	rm -rf build
	rm -rf dist
	rm README.rst
