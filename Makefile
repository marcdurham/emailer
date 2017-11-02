upload:
	./setup.py sdist bdist_wheel && twine upload dist/*

clean:
	rm dist/*
