dev:
	pip install -e .

upload: setup clean

setup:
	./setup.py sdist bdist_wheel && twine upload dist/*

clean:
	rm dist/*
