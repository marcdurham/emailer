.PHONY: dev full test lint integration upload clean
dev:
	pip install -U -r requirements.txt
	pip install -U -e .
	ctags

full: test integration lint

test:
	tests/unit_test.py

lint:
	pylint emailer tests/*.py

integration:
	tests/integration_test.py

upload: full
	./setup.py sdist bdist_wheel
	twine upload dist/*
	make clean

clean:
	rm -rf build
	rm -rf dist
