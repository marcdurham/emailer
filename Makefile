dev:
	pip install -e .

full: test integration_test lint

test: unit_test lint

integration_test:
	tests/integration_test.py

unit_test:
	tests/unit_test.py

lint:
	pylint emailer tests/*.py

upload: setup clean

setup:
	pandoc README.md --from markdown --to rst -s -o README.rst
	./setup.py sdist bdist_wheel && twine upload dist/*

clean:
	rm dist/*
	rm README.rst
