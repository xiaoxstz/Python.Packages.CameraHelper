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

# clean all the temporary files
clean_temp:
	rm -rf ./src/build
	rm -rf src/*.egg-info

# Run multiple make commands. Please put them in a row
all:clean build_dist build clean_temp
