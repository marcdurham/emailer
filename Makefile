dev:
	pip install -e .

test: unit_test

full_test: test integration_test

integration_test:
	tests/integration_test.py

unit_test:
	tests/unit_test.py

upload: setup clean

setup:
	pandoc README.md --from markdown --to rst -s -o README.rst
	./setup.py sdist bdist_wheel && twine upload dist/*

clean:
	rm dist/*
	rm README.rst
