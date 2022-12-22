build:
	python -m build

build_dist:
	python setup.py build_ext --inplace

clean:
	rm -rf dist
	rm -rf ./src/build
	rm -rf src/*.egg-info