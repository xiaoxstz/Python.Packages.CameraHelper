build:
	python -m build

build_dist:
	cd ./src &&\
	python setup.py build_ext --inplace

clean:
	rm -rf dist
	rm -rf ./src/build
	rm -rf src/*.egg-info