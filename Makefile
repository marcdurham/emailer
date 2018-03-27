dev:
	pip install -e .

upload: setup clean

setup:
	pandoc README.md --from markdown --to rst -s -o README.rst
	./setup.py sdist bdist_wheel && twine upload dist/*

clean:
	rm dist/*
	rm README.rst
