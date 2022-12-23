# build the wheel file
build:
	python -m build

# build into binary files
bin:
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

# Run unit test
test:
	python -m unittest

# check code
# flake8: pip install flake8
lint:
	flake8 src/ tests/ examples/ --count --statistics

# only check Error(E) and Fatal(F)
error:
	flake8 --select E,F --ignore=E501 src/ tests/ examples/ --count --statistics --exclude=src/*/__init__.py

# formatters choices:black,autopep8,prettier,yapf
format:
	black src/ tests/ examples/

# Run multiple make commands. Please put them in a row
all:clean build_dist build clean_temp
