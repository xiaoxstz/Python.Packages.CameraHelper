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

# clean all the temporary files
clean_temp:
	rm -rf ./src/build
	rm -rf src/*.egg-info
	rm -rf */__pycache__
	rm -rf src/*.pyi
	rm -rf src/*/__pycache__
	rm -rf src/*/*.c
	rm -rf src/*/*.pyd
	rm -rf src/*/*.pyi

# Run unit test
test:
	python -m unittest

# check code
# flake8: pip install flake8
lint:
	make format
	flake8 --ignore=E501 src/ tests/ examples/ --count --statistics --exclude=src/*/__init__.py

# only check Error(E) and Fatal(F)
error:
	make format
	flake8 --select E,F --ignore=E501 src/ tests/ examples/ --count --statistics --exclude=src/*/__init__.py

# formatters choices:black,autopep8,prettier,yapf
format:
	black src/ tests/ examples/

# generate files for IDE's code hint if replacing .py files with .pyd files
# pip install mypy
stub:
	stubgen src/ -o src/

# Run multiple make commands. Please put them in a row
# all:clean bin build clean_temp
all:stub bin build
