dev:
	pip install -U -r requirements.txt
	pip install -U -e .

full: test integration_test lint

test: unit_test

lint: pylint

integration_test:
	# TODO: Fix crash
	#tests/integration_test.py

unit_test:
	tests/unit_test.py

pylint:
	pylint emailer tests/*.py

upload: full setup pypi clean

setup:
	./setup.py sdist bdist_wheel

pypi:
	twine upload dist/*

clean:
	rm -rf build
	rm -rf dist
