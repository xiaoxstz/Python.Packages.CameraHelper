# build the wheel file
build:
	python -m build

# build into binary files
build_dist:
	cd ./src &&\
	python setup.py build_ext --inplace

# clean all the generated files
clean:
	make clean_temp
	rm -rf dist
	rm -rf */__pycache__

# clean all the temporary files
clean_temp:
	rm -rf ./src/build
	rm -rf src/*.egg-info
	rm -rf src/*/__pycache__
	rm -rf src/*/*.c
	rm -rf src/*/*.pyd

test:
	python -m unittest

# Run multiple make commands. Please put them in a row
all:clean build_dist build clean_temp
