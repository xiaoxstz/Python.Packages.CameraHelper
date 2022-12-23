
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [1. Build steps](#1-build-steps)
  - [1.1. firstly,build into binary files](#11-firstlybuild-into-binary-files)
  - [1.2. secondly,build the wheel file](#12-secondlybuild-the-wheel-file)
- [2. Build with Makefile](#2-build-with-makefile)

<!-- /code_chunk_output -->

# 1. Build steps
## 1.1. firstly,build into binary files
Firstly,ensure the terminal path is `.\src`

Then, use the command below to compile the `.py` files to `.pyd` files

`python setup.py build_ext --inplace`

## 1.2. secondly,build the wheel file
Firstly,ensure the terminal path is the root folder

```bash
python -m build
```
then it will create a folder `dist` and a folder `mypackage.egg-info`
* there are `*.tar.gz` and `*.whl` in the folder `dist`

You have to ensure the internet is fine when running this command.Because it needs internet to install the packages to the isolated environment,according to the output message below.
  ```txt
  * Creating venv isolated environment...
  * Installing packages in isolated environment... (setuptools>=42, wheel) 
  ```
# 2. Build with Makefile
Makefile provides the commands below
* `make bin`: build into binary files
* `make build`: build the wheel file
* `make all`: run the comands at one time. When it completes, we can find the wheel in the folder `dist`
* `make clean_temp`: clean all the temporary files
* `make clean`: clean all the generated files
* Others: see `Makefile`
