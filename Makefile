setup:
	./setup.py sdist bdist_wheel && twine upload dist/*

clean:
	rm dist/*

dev:
	pip install -e .

upload: setup clean
